from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pyodbc
import pandas as pd
import io
from datetime import datetime

app = FastAPI()

# --- 配置 CORS (解决前后端跨域问题) ---
# React 默认运行在 localhost:5173，必须允许它访问后端
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许所有来源，开发阶段方便
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 数据库连接配置 ---
# 注意：SERVER=./ 或 SERVER=localhost 通常可行，不行则填你的计算机名
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;" 
    "DATABASE=GradeSystemDB;"
    "Trusted_Connection=yes;"
)

def get_db_connection():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"数据库连接失败: {e}")
        raise HTTPException(status_code=500, detail="数据库连接失败")

# --- Pydantic 数据模型 (用于验证前端请求) ---

class LoginRequest(BaseModel):
    username: str
    password: str

class GradeInput(BaseModel):
    student_id: int
    course_id: int
    regular_score: float
    midterm_score: float
    final_score: float

class ScholarshipParams(BaseModel):
    year: int
    term: int

# --- API 接口编写 ---

# 1. 根路径测试
@app.get("/")
def read_root():
    return {"message": "学生成绩管理系统后端已启动"}

# 2. 登录接口 (简单的模拟验证)
@app.post("/api/login")
def login(request: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 先检查用户是否存在
        cursor.execute("SELECT UserID, Role, RelatedID, PasswordHash FROM Users WHERE Username=?", 
                       (request.username,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        
        # 检查密码（这里是明文比较，实际项目应该用哈希）
        if user.PasswordHash != request.password:
            raise HTTPException(status_code=401, detail="密码错误")
        
        return {"status": "success", "role": user.Role, "related_id": user.RelatedID}
        
    except Exception as e:
        print(f"登录错误: {e}")
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")
    finally:
        conn.close()

# 添加测试接口
@app.get("/api/test/users")
def test_users():
    """测试接口：查看所有用户"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Username, Role, RelatedID FROM Users")
        users = cursor.fetchall()
        result = []
        for user in users:
            result.append({
                "username": user[0],
                "role": user[1], 
                "related_id": user[2]
            })
        return {"users": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 3. 老师录入成绩
@app.post("/api/grades/add")
def add_grade(data: GradeInput):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 检查是否已存在，存在则更新，不存在则插入
        # 这里为了简化，直接用 MERGE 或 简单的 IF EXISTS 逻辑
        # 也可以直接插入，依赖数据库的 UNIQUE 约束报错
        sql = """
        IF EXISTS (SELECT 1 FROM Grades WHERE StudentID=? AND CourseID=?)
            UPDATE Grades SET RegularScore=?, MidtermScore=?, FinalScore=? 
            WHERE StudentID=? AND CourseID=?
        ELSE
            INSERT INTO Grades (StudentID, CourseID, RegularScore, MidtermScore, FinalScore)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, 
                       (data.student_id, data.course_id, data.regular_score, data.midterm_score, data.final_score,
                        data.student_id, data.course_id,
                        data.student_id, data.course_id, data.regular_score, data.midterm_score, data.final_score))
        conn.commit()
        return {"message": "成绩录入成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# 4. [核心功能] 一键结算奖学金 (调用存储过程)
@app.post("/api/scholarship/settle")
def settle_scholarship(params: ScholarshipParams):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 调用我们在 SQL Server 里写的存储过程
        sql = "{CALL sp_CalculateScholarship (?, ?)}"
        cursor.execute(sql, (params.year, params.term))
        conn.commit()
        return {"message": f"{params.year}学年第{params.term}学期奖学金计算完成"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 5. [核心功能] 导出 Excel (Pandas)
@app.get("/api/export/grades")
def export_grades(class_id: Optional[int] = None):
    conn = get_db_connection()
    
    # 老师可以导出全班，通过 class_id 筛选，或者导出所有
    if class_id:
        query = """
            SELECT s.StudentID, s.Name, c.ClassName, co.CourseName, g.TotalScore
            FROM Grades g
            JOIN Students s ON g.StudentID = s.StudentID
            JOIN Classes c ON s.ClassID = c.ClassID
            JOIN Courses co ON g.CourseID = co.CourseID
            WHERE s.ClassID = ?
        """
        df = pd.read_sql(query, conn, params=(class_id,))
    else:
        query = "SELECT * FROM Grades" # 简化，实际应关联表名
        df = pd.read_sql(query, conn)
    
    conn.close()
    
    # 将 DataFrame 写入内存中的 Excel 文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='成绩单')
    
    output.seek(0)
    
    # 返回文件流
    headers = {
        'Content-Disposition': 'attachment; filename="grades_export.xlsx"'
    }
    return Response(content=output.getvalue(), headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    import uvicorn
    # 启动服务器，端口 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
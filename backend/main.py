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

class ComprehensiveEvaluationInput(BaseModel):
    student_id: int
    academic_year: str
    semester: int
    physical_score: Optional[float] = None
    moral_score: Optional[float] = None
    gpa: Optional[float] = None
    academic_score: Optional[float] = None
    innovation_basic_score: Optional[float] = None
    innovation_bonus_score: Optional[float] = None
    student_work_score: Optional[float] = None
    social_service_score: Optional[float] = None
    social_reward_score: Optional[float] = None
    cultural_sports_score: Optional[float] = None

class BonusDetailInput(BaseModel):
    evaluation_id: int
    category: str
    item_name: str
    score: float
    description: Optional[str] = None

class RankingParams(BaseModel):
    academic_year: str
    semester: int

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

# 3. 录入综合测评数据
@app.post("/api/evaluation/add")
def add_evaluation(data: ComprehensiveEvaluationInput):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
        IF EXISTS (SELECT 1 FROM ComprehensiveEvaluations WHERE StudentID=? AND AcademicYear=? AND Semester=?)
            UPDATE ComprehensiveEvaluations SET 
                PhysicalScore=?, MoralScore=?, GPA=?, AcademicScore=?,
                InnovationBasicScore=?, InnovationBonusScore=?,
                StudentWorkScore=?, SocialServiceScore=?, SocialRewardScore=?,
                CulturalSportsScore=?, UpdatedAt=GETDATE()
            WHERE StudentID=? AND AcademicYear=? AND Semester=?
        ELSE
            INSERT INTO ComprehensiveEvaluations (
                StudentID, AcademicYear, Semester, PhysicalScore, MoralScore, GPA, AcademicScore,
                InnovationBasicScore, InnovationBonusScore, StudentWorkScore, 
                SocialServiceScore, SocialRewardScore, CulturalSportsScore
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, 
                       (data.student_id, data.academic_year, data.semester,
                        data.physical_score, data.moral_score, data.gpa, data.academic_score,
                        data.innovation_basic_score, data.innovation_bonus_score,
                        data.student_work_score, data.social_service_score, data.social_reward_score,
                        data.cultural_sports_score,
                        data.student_id, data.academic_year, data.semester,
                        data.student_id, data.academic_year, data.semester,
                        data.physical_score, data.moral_score, data.gpa, data.academic_score,
                        data.innovation_basic_score, data.innovation_bonus_score,
                        data.student_work_score, data.social_service_score, data.social_reward_score,
                        data.cultural_sports_score))
        conn.commit()
        return {"message": "综合测评数据录入成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# 4. 添加加分项目
@app.post("/api/bonus/add")
def add_bonus_detail(data: BonusDetailInput):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO BonusDetails (EvaluationID, Category, ItemName, Score, Description)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (data.evaluation_id, data.category, data.item_name, 
                           data.score, data.description))
        conn.commit()
        return {"message": "加分项目添加成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# 5. 计算排名
@app.post("/api/ranking/calculate")
def calculate_rankings(params: RankingParams):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "{CALL sp_CalculateRankings (?, ?)}"
        cursor.execute(sql, (params.academic_year, params.semester))
        conn.commit()
        return {"message": f"{params.academic_year}学年第{params.semester}学期排名计算完成"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 6. 获取综测排名
@app.get("/api/ranking/list")
def get_rankings(academic_year: str, semester: int, limit: Optional[int] = 50):
    conn = get_db_connection()
    try:
        query = """
            SELECT TOP (?) 
                ClassRank, StudentName, TotalScore, GPA, AcademicScore,
                InnovationTotalScore, SocialTotalScore, CulturalSportsScore
            FROM v_ComprehensiveEvaluationDetails
            WHERE AcademicYear = ? AND Semester = ?
            ORDER BY ClassRank
        """
        df = pd.read_sql(query, conn, params=(limit, academic_year, semester))
        return {"rankings": df.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 7. 获取学生详细信息
@app.get("/api/student/{student_id}")
def get_student_detail(student_id: int, academic_year: str, semester: int):
    conn = get_db_connection()
    try:
        # 获取基本信息
        query = """
            SELECT * FROM v_ComprehensiveEvaluationDetails
            WHERE StudentID = ? AND AcademicYear = ? AND Semester = ?
        """
        df = pd.read_sql(query, conn, params=(student_id, academic_year, semester))
        
        if df.empty:
            raise HTTPException(status_code=404, detail="学生数据不存在")
        
        student_info = df.iloc[0].to_dict()
        
        # 获取加分项目
        bonus_query = """
            SELECT bd.Category, bd.ItemName, bd.Score, bd.Description
            FROM BonusDetails bd
            JOIN ComprehensiveEvaluations ce ON bd.EvaluationID = ce.EvaluationID
            WHERE ce.StudentID = ? AND ce.AcademicYear = ? AND ce.Semester = ?
        """
        bonus_df = pd.read_sql(bonus_query, conn, params=(student_id, academic_year, semester))
        student_info['bonus_details'] = bonus_df.to_dict('records')
        
        return student_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# 8. [核心功能] 导出综测Excel
@app.get("/api/export/comprehensive")
def export_comprehensive(academic_year: str, semester: int, class_id: Optional[int] = None):
    conn = get_db_connection()
    
    if class_id:
        query = """
            SELECT 
                ClassRank as 班级排名,
                StudentID as 学号,
                StudentName as 姓名,
                ClassName as 班级,
                PhysicalScore as 体测成绩,
                MoralScore as 品德表现,
                GPA as 绩点,
                AcademicScore as 学业成绩,
                InnovationTotalScore as 创新实践,
                SocialTotalScore as 社会实践,
                CulturalSportsScore as 文体实践,
                TotalScore as 总积分
            FROM v_ComprehensiveEvaluationDetails
            WHERE AcademicYear = ? AND Semester = ? AND StudentID IN (
                SELECT StudentID FROM Students WHERE ClassID = ?
            )
            ORDER BY ClassRank
        """
        df = pd.read_sql(query, conn, params=(academic_year, semester, class_id))
    else:
        query = """
            SELECT 
                GradeRank as 年级排名,
                ClassRank as 班级排名,
                StudentID as 学号,
                StudentName as 姓名,
                ClassName as 班级,
                PhysicalScore as 体测成绩,
                MoralScore as 品德表现,
                GPA as 绩点,
                AcademicScore as 学业成绩,
                InnovationTotalScore as 创新实践,
                SocialTotalScore as 社会实践,
                CulturalSportsScore as 文体实践,
                TotalScore as 总积分
            FROM v_ComprehensiveEvaluationDetails
            WHERE AcademicYear = ? AND Semester = ?
            ORDER BY GradeRank
        """
        df = pd.read_sql(query, conn, params=(academic_year, semester))
    
    conn.close()
    
    # 将 DataFrame 写入内存中的 Excel 文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=f'{academic_year}学年第{semester}学期综测')
    
    output.seek(0)
    
    # 返回文件流
    headers = {
        'Content-Disposition': f'attachment; filename="comprehensive_evaluation_{academic_year}_S{semester}.xlsx"'
    }
    return Response(content=output.getvalue(), headers=headers, 
                   media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    import uvicorn
    # 启动服务器，端口 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
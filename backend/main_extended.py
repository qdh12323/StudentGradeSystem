from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pyodbc
import pandas as pd
import io
from datetime import datetime

app = FastAPI()

# --- 配置 CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 数据库连接配置 ---
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

# --- Pydantic 数据模型 ---

class LoginRequest(BaseModel):
    username: str
    password: str

class StudentInput(BaseModel):
    student_id: int
    name: str
    class_id: int
    major: str
    gender: Optional[str] = None
    birthdate: Optional[str] = None
    hometown: Optional[str] = None
    id_card: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[str] = None
    status: Optional[str] = "在读"

class CourseInput(BaseModel):
    course_code: str
    course_name: str
    credits: float
    hours: int
    course_type: Optional[str] = "必修"
    department: Optional[str] = None
    prerequisites: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = "开设"

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

# --- API 接口 ---

@app.get("/")
def read_root():
    return {"message": "学生成绩管理系统后端已启动 - 扩展版"}

# === 用户认证相关 ===

@app.post("/api/login")
def login(request: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT UserID, Role, RelatedID, PasswordHash FROM Users WHERE Username=?", 
                       (request.username,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        
        if user.PasswordHash != request.password:
            raise HTTPException(status_code=401, detail="密码错误")
        
        return {"status": "success", "role": user.Role, "related_id": user.RelatedID}
        
    except Exception as e:
        print(f"登录错误: {e}")
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")
    finally:
        conn.close()

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

# === 学生信息管理 ===

@app.post("/api/students/add")
def add_student(data: StudentInput):
    """新增学生"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 检查学号是否已存在
        cursor.execute("SELECT COUNT(*) FROM Students WHERE StudentID = ?", (data.student_id,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="学号已存在")
        
        sql = """
        INSERT INTO Students (
            StudentID, Name, ClassID, Major, Gender, Birthdate, Hometown, 
            IDCard, Phone, Email, Address, EnrollmentDate, Status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            data.student_id, data.name, data.class_id, data.major, data.gender,
            data.birthdate, data.hometown, data.id_card, data.phone, data.email,
            data.address, data.enrollment_date, data.status
        ))
        
        # 创建用户账号
        cursor.execute("""
            INSERT INTO Users (Username, PasswordHash, Role, RelatedID)
            VALUES (?, '123456', 'Student', ?)
        """, (str(data.student_id), data.student_id))
        
        conn.commit()
        return {"message": "学生添加成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/students/list")
def get_students(page: int = 1, size: int = 20, search: Optional[str] = None):
    """获取学生列表"""
    conn = get_db_connection()
    try:
        offset = (page - 1) * size
        
        where_clause = ""
        params = []
        if search:
            where_clause = "WHERE s.Name LIKE ? OR CAST(s.StudentID AS NVARCHAR) LIKE ? OR c.ClassName LIKE ?"
            search_param = f"%{search}%"
            params = [search_param, search_param, search_param]
        
        # 获取总数
        count_sql = f"""
            SELECT COUNT(*) FROM Students s
            LEFT JOIN Classes c ON s.ClassID = c.ClassID
            {where_clause}
        """
        total = pd.read_sql(count_sql, conn, params=params).iloc[0, 0]
        
        # 获取数据
        data_sql = f"""
            SELECT 
                s.StudentID, s.Name, s.Major, s.Gender, s.Hometown, s.Phone, 
                s.Email, s.EnrollmentDate, s.Status, c.ClassName,
                s.CreatedAt, s.UpdatedAt
            FROM Students s
            LEFT JOIN Classes c ON s.ClassID = c.ClassID
            {where_clause}
            ORDER BY s.StudentID
            OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
        """
        params.extend([offset, size])
        df = pd.read_sql(data_sql, conn, params=params)
        
        return {
            "students": df.to_dict('records'),
            "total": int(total),
            "page": page,
            "size": size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/api/students/{student_id}")
def update_student(student_id: int, data: StudentInput):
    """修改学生信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
        UPDATE Students SET 
            Name=?, ClassID=?, Major=?, Gender=?, Birthdate=?, Hometown=?,
            IDCard=?, Phone=?, Email=?, Address=?, EnrollmentDate=?, Status=?,
            UpdatedAt=GETDATE()
        WHERE StudentID=?
        """
        cursor.execute(sql, (
            data.name, data.class_id, data.major, data.gender, data.birthdate,
            data.hometown, data.id_card, data.phone, data.email, data.address,
            data.enrollment_date, data.status, student_id
        ))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="学生不存在")
        
        conn.commit()
        return {"message": "学生信息更新成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.delete("/api/students/{student_id}")
def delete_student(student_id: int):
    """删除学生（逻辑删除）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 逻辑删除，设置状态为已删除
        cursor.execute("""
            UPDATE Students SET Status='已删除', UpdatedAt=GETDATE() 
            WHERE StudentID=?
        """, (student_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="学生不存在")
        
        # 禁用用户账号
        cursor.execute("""
            UPDATE Users SET PasswordHash='DISABLED' 
            WHERE RelatedID=? AND Role='Student'
        """, (student_id,))
        
        conn.commit()
        return {"message": "学生删除成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# === 课程信息管理 ===

@app.post("/api/courses/add")
def add_course(data: CourseInput):
    """新增课程"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # 检查课程编号是否已存在
        cursor.execute("SELECT COUNT(*) FROM Courses WHERE CourseCode = ?", (data.course_code,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="课程编号已存在")
        
        sql = """
        INSERT INTO Courses (
            CourseCode, CourseName, Credits, Hours, CourseType, 
            Department, Prerequisites, Description, Status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            data.course_code, data.course_name, data.credits, data.hours,
            data.course_type, data.department, data.prerequisites, 
            data.description, data.status
        ))
        
        conn.commit()
        return {"message": "课程添加成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.get("/api/courses/list")
def get_courses(page: int = 1, size: int = 20, search: Optional[str] = None):
    """获取课程列表"""
    conn = get_db_connection()
    try:
        offset = (page - 1) * size
        
        where_clause = ""
        params = []
        if search:
            where_clause = "WHERE CourseCode LIKE ? OR CourseName LIKE ? OR Department LIKE ?"
            search_param = f"%{search}%"
            params = [search_param, search_param, search_param]
        
        # 获取总数
        count_sql = f"SELECT COUNT(*) FROM Courses {where_clause}"
        total = pd.read_sql(count_sql, conn, params=params).iloc[0, 0]
        
        # 获取数据
        data_sql = f"""
            SELECT 
                CourseID, CourseCode, CourseName, Credits, Hours, CourseType,
                Department, Prerequisites, Description, Status, CreatedAt, UpdatedAt
            FROM Courses
            {where_clause}
            ORDER BY CourseCode
            OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
        """
        params.extend([offset, size])
        df = pd.read_sql(data_sql, conn, params=params)
        
        return {
            "courses": df.to_dict('records'),
            "total": int(total),
            "page": page,
            "size": size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/api/courses/{course_id}")
def update_course(course_id: int, data: CourseInput):
    """修改课程信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = """
        UPDATE Courses SET 
            CourseCode=?, CourseName=?, Credits=?, Hours=?, CourseType=?,
            Department=?, Prerequisites=?, Description=?, Status=?, UpdatedAt=GETDATE()
        WHERE CourseID=?
        """
        cursor.execute(sql, (
            data.course_code, data.course_name, data.credits, data.hours,
            data.course_type, data.department, data.prerequisites,
            data.description, data.status, course_id
        ))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="课程不存在")
        
        conn.commit()
        return {"message": "课程信息更新成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

@app.delete("/api/courses/{course_id}")
def delete_course(course_id: int):
    """删除课程（逻辑删除）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE Courses SET Status='已停开', UpdatedAt=GETDATE() 
            WHERE CourseID=?
        """, (course_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="课程不存在")
        
        conn.commit()
        return {"message": "课程删除成功"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# === 综合测评相关（保持原有功能） ===

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

@app.get("/api/ranking/list")
def get_rankings(academic_year: str, semester: int, limit: Optional[int] = 50, role: Optional[str] = None):
    conn = get_db_connection()
    try:
        # 学生角色只能看前10名
        if role == 'Student' and (limit is None or limit > 10):
            limit = 10
            
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

@app.get("/api/student/{student_id}")
def get_student_detail(student_id: int, academic_year: str, semester: int):
    conn = get_db_connection()
    try:
        query = """
            SELECT * FROM v_ComprehensiveEvaluationDetails
            WHERE StudentID = ? AND AcademicYear = ? AND Semester = ?
        """
        df = pd.read_sql(query, conn, params=(student_id, academic_year, semester))
        
        if df.empty:
            raise HTTPException(status_code=404, detail="学生数据不存在")
        
        student_info = df.iloc[0].to_dict()
        
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
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=f'{academic_year}学年第{semester}学期综测')
    
    output.seek(0)
    
    headers = {
        'Content-Disposition': f'attachment; filename="comprehensive_evaluation_{academic_year}_S{semester}.xlsx"'
    }
    return Response(content=output.getvalue(), headers=headers, 
                   media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
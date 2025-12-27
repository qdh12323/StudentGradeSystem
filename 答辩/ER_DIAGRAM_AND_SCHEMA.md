# 大数据2班管理系统 - ER图与关系模式

## 项目概述

**系统名称**: 大数据2班管理系统  
**开发团队**: 2024级数据科学与大数据技术2班  
**技术栈**: React + FastAPI + SQL Server  
**GitHub**: https://github.com/qdh12323/StudentGradeSystem

## 1. 实体关系图 (ER Diagram)

### 1.1 主要实体

#### 🎓 学生 (Students)
- **StudentID** (主键): 学号 (BIGINT)
- Name: 姓名
- Gender: 性别
- Birthdate: 出生日期
- Hometown: 籍贯
- IDCard: 身份证号
- Phone: 联系电话
- Email: 邮箱
- Address: 家庭住址
- ClassID: 班级ID (外键)
- EnrollmentDate: 入学日期
- Status: 学生状态

#### 📚 课程 (Courses)
- **CourseID** (主键): 课程ID
- CourseCode: 课程编号 (唯一)
- CourseName: 课程名称
- Credits: 学分
- Hours: 学时
- CourseType: 课程类型 (必修/选修)
- Department: 开课院系
- Prerequisites: 先修课程
- Description: 课程描述
- Status: 课程状态

#### 🏫 班级 (Classes)
- **ClassID** (主键): 班级ID
- ClassName: 班级名称
- Major: 专业
- Grade: 年级
- Advisor: 班主任

#### 📊 综合测评 (ComprehensiveEvaluations)
- **EvaluationID** (主键): 评估ID
- StudentID: 学号 (外键)
- AcademicYear: 学年
- Semester: 学期
- PhysicalScore: 体测成绩 (T)
- MoralScore: 品德表现评价分 (D)
- GPA: 绩点
- AcademicScore: 学业成绩考核分 (X)
- InnovationBasicScore: 创新实践基本分 (C1)
- InnovationBonusScore: 创新实践加分 (C2)
- InnovationTotalScore: 创新实践总分 (C)
- StudentWorkScore: 学生工作加分 (S1)
- SocialServiceScore: 社会服务加分 (S2)
- SocialRewardScore: 社会服务奖励加分 (S3)
- SocialTotalScore: 社会实践总分 (S)
- CulturalSportsScore: 文体实践评分 (W)
- TotalScore: 总积分 (P)
- ClassRank: 班级排名
- GradeRank: 年级排名

#### 🎯 加分详情 (BonusDetails)
- **DetailID** (主键): 详情ID
- EvaluationID: 评估ID (外键)
- Category: 加分类别 (C1/C2/S1/S2/S3/W)
- ItemName: 加分项目名称
- Score: 加分分数
- Description: 详细描述
- Evidence: 证明材料
- Status: 审核状态

#### 📖 课程开设 (CourseOfferings)
- **OfferingID** (主键): 开设ID
- CourseID: 课程ID (外键)
- TeacherName: 授课教师
- AcademicYear: 学年
- Semester: 学期
- ClassTime: 上课时间
- Classroom: 教室
- MaxStudents: 最大选课人数
- CurrentStudents: 当前选课人数

#### 👤 用户 (Users)
- **UserID** (主键): 用户ID
- Username: 用户名 (唯一)
- PasswordHash: 密码哈希
- Role: 角色 (Student/Teacher/Admin)
- RelatedID: 关联ID (学生ID或教师ID)

### 1.2 实体关系

```
学生 (Students) ──┐
                 │ 1:N
                 ├── 综合测评 (ComprehensiveEvaluations)
                 │                │ 1:N
                 │                └── 加分详情 (BonusDetails)
                 │
                 │ N:1
                 └── 班级 (Classes)

课程 (Courses) ──┐ 1:N
                └── 课程开设 (CourseOfferings)

用户 (Users) ──── 关联 ──── 学生 (Students)
```

## 2. 关系模式 (Relational Schema)

### 2.1 基本关系模式

#### R1: Students (学生表)
```sql
Students(
    StudentID: BIGINT [PK],           -- 学号，主键
    Name: NVARCHAR(50) [NOT NULL],   -- 姓名，非空
    Gender: NVARCHAR(10),            -- 性别
    Birthdate: DATE,                 -- 出生日期
    Hometown: NVARCHAR(100),         -- 籍贯
    IDCard: NVARCHAR(18),            -- 身份证号
    Phone: NVARCHAR(20),             -- 联系电话
    Email: NVARCHAR(100),            -- 邮箱
    Address: NVARCHAR(200),          -- 家庭住址
    ClassID: INT [FK → Classes.ClassID], -- 班级ID，外键
    EnrollmentDate: DATE,            -- 入学日期
    Status: NVARCHAR(20) [DEFAULT '在读'], -- 学生状态
    CreatedAt: DATETIME [DEFAULT GETDATE()],
    UpdatedAt: DATETIME [DEFAULT GETDATE()]
)
```

#### R2: Classes (班级表)
```sql
Classes(
    ClassID: INT [PK, IDENTITY],     -- 班级ID，主键，自增
    ClassName: NVARCHAR(100) [NOT NULL], -- 班级名称，非空
    Major: NVARCHAR(100) [NOT NULL], -- 专业，非空
    Grade: INT [NOT NULL],           -- 年级，非空
    Advisor: NVARCHAR(50),           -- 班主任
    CreatedAt: DATETIME [DEFAULT GETDATE()]
)
```

#### R3: Courses (课程表)
```sql
Courses(
    CourseID: INT [PK, IDENTITY],    -- 课程ID，主键，自增
    CourseCode: NVARCHAR(20) [UNIQUE, NOT NULL], -- 课程编号，唯一，非空
    CourseName: NVARCHAR(100) [NOT NULL], -- 课程名称，非空
    Credits: DECIMAL(3,1) [NOT NULL], -- 学分，非空
    Hours: INT [NOT NULL],           -- 学时，非空
    CourseType: NVARCHAR(20) [DEFAULT '必修'], -- 课程类型
    Department: NVARCHAR(50),        -- 开课院系
    Prerequisites: NVARCHAR(200),    -- 先修课程
    Description: NTEXT,              -- 课程描述
    Status: NVARCHAR(20) [DEFAULT '开设'], -- 课程状态
    CreatedAt: DATETIME [DEFAULT GETDATE()],
    UpdatedAt: DATETIME [DEFAULT GETDATE()]
)
```

#### R4: ComprehensiveEvaluations (综合测评表)
```sql
ComprehensiveEvaluations(
    EvaluationID: INT [PK, IDENTITY], -- 评估ID，主键，自增
    StudentID: BIGINT [FK → Students.StudentID, NOT NULL], -- 学号，外键，非空
    AcademicYear: NVARCHAR(20) [NOT NULL], -- 学年，非空
    Semester: INT [NOT NULL],        -- 学期，非空
    PhysicalScore: DECIMAL(5,2),     -- 体测成绩 (T)
    MoralScore: DECIMAL(5,2),        -- 品德表现评价分 (D)
    GPA: DECIMAL(4,2),               -- 绩点
    AcademicScore: DECIMAL(6,2),     -- 学业成绩考核分 (X)
    InnovationBasicScore: DECIMAL(5,2), -- 创新实践基本分 (C1)
    InnovationBonusScore: DECIMAL(5,2), -- 创新实践加分 (C2)
    InnovationTotalScore: DECIMAL(5,2), -- 创新实践总分 (C)
    StudentWorkScore: DECIMAL(5,2),  -- 学生工作加分 (S1)
    SocialServiceScore: DECIMAL(5,2), -- 社会服务加分 (S2)
    SocialRewardScore: DECIMAL(5,2), -- 社会服务奖励加分 (S3)
    SocialTotalScore: DECIMAL(5,2),  -- 社会实践总分 (S)
    CulturalSportsScore: DECIMAL(5,2), -- 文体实践评分 (W)
    TotalScore: DECIMAL(7,2),        -- 总积分 (P)
    ClassRank: INT,                  -- 班级排名
    GradeRank: INT,                  -- 年级排名
    CreatedAt: DATETIME [DEFAULT GETDATE()],
    UpdatedAt: DATETIME [DEFAULT GETDATE()],
    UNIQUE(StudentID, AcademicYear, Semester) -- 唯一约束
)
```

#### R5: BonusDetails (加分详情表)
```sql
BonusDetails(
    DetailID: INT [PK, IDENTITY],    -- 详情ID，主键，自增
    EvaluationID: INT [FK → ComprehensiveEvaluations.EvaluationID, NOT NULL], -- 评估ID，外键，非空
    Category: NVARCHAR(20) [NOT NULL], -- 加分类别，非空
    ItemName: NVARCHAR(200) [NOT NULL], -- 加分项目名称，非空
    Score: DECIMAL(5,2) [NOT NULL],  -- 加分分数，非空
    Description: NVARCHAR(500),      -- 详细描述
    Evidence: NVARCHAR(200),         -- 证明材料
    Status: NVARCHAR(20) [DEFAULT '已审核'], -- 审核状态
    CreatedAt: DATETIME [DEFAULT GETDATE()]
)
```

#### R6: CourseOfferings (课程开设表)
```sql
CourseOfferings(
    OfferingID: INT [PK, IDENTITY],  -- 开设ID，主键，自增
    CourseID: INT [FK → Courses.CourseID, NOT NULL], -- 课程ID，外键，非空
    TeacherName: NVARCHAR(50),       -- 授课教师
    AcademicYear: NVARCHAR(20),      -- 学年
    Semester: INT,                   -- 学期
    ClassTime: NVARCHAR(100),        -- 上课时间
    Classroom: NVARCHAR(50),         -- 教室
    MaxStudents: INT [DEFAULT 50],   -- 最大选课人数
    CurrentStudents: INT [DEFAULT 0], -- 当前选课人数
    CreatedAt: DATETIME [DEFAULT GETDATE()]
)
```

#### R7: Users (用户表)
```sql
Users(
    UserID: INT [PK, IDENTITY],      -- 用户ID，主键，自增
    Username: NVARCHAR(50) [UNIQUE, NOT NULL], -- 用户名，唯一，非空
    PasswordHash: NVARCHAR(255) [NOT NULL], -- 密码哈希，非空
    Role: NVARCHAR(20) [NOT NULL],   -- 角色，非空
    RelatedID: BIGINT,               -- 关联ID
    CreatedAt: DATETIME [DEFAULT GETDATE()]
)
```

### 2.2 函数依赖

#### Students表的函数依赖
- StudentID → Name, Gender, Birthdate, Hometown, IDCard, Phone, Email, Address, ClassID, EnrollmentDate, Status
- IDCard → StudentID (身份证号唯一确定学生)

#### Classes表的函数依赖
- ClassID → ClassName, Major, Grade, Advisor
- ClassName → ClassID (班级名称唯一)

#### Courses表的函数依赖
- CourseID → CourseCode, CourseName, Credits, Hours, CourseType, Department, Prerequisites, Description, Status
- CourseCode → CourseID (课程编号唯一确定课程)

#### ComprehensiveEvaluations表的函数依赖
- EvaluationID → StudentID, AcademicYear, Semester, PhysicalScore, ..., TotalScore, ClassRank, GradeRank
- (StudentID, AcademicYear, Semester) → EvaluationID (学生在特定学年学期的评估唯一)

### 2.3 范式分析

#### 第一范式 (1NF)
✅ **满足**: 所有表的属性都是原子性的，不可再分。

#### 第二范式 (2NF)
✅ **满足**: 所有表都有单一主键，非主属性完全函数依赖于主键。

#### 第三范式 (3NF)
✅ **满足**: 消除了传递依赖，非主属性不依赖于其他非主属性。

#### BC范式 (BCNF)
✅ **满足**: 每个函数依赖的左边都包含候选键。

## 3. 约束条件

### 3.1 主键约束
- Students.StudentID (主键)
- Classes.ClassID (主键)
- Courses.CourseID (主键)
- ComprehensiveEvaluations.EvaluationID (主键)
- BonusDetails.DetailID (主键)
- CourseOfferings.OfferingID (主键)
- Users.UserID (主键)

### 3.2 外键约束
- Students.ClassID → Classes.ClassID
- ComprehensiveEvaluations.StudentID → Students.StudentID
- BonusDetails.EvaluationID → ComprehensiveEvaluations.EvaluationID
- CourseOfferings.CourseID → Courses.CourseID

### 3.3 唯一性约束
- Courses.CourseCode (课程编号唯一)
- Users.Username (用户名唯一)
- (ComprehensiveEvaluations.StudentID, AcademicYear, Semester) (学生在特定学年学期的评估唯一)

### 3.4 检查约束
- ComprehensiveEvaluations.Semester IN (1, 2) (学期只能是1或2)
- Students.Status IN ('在读', '休学', '退学', '毕业') (学生状态限制)
- Courses.CourseType IN ('必修', '选修') (课程类型限制)
- Users.Role IN ('Student', 'Teacher', 'Admin') (用户角色限制)

## 4. 索引设计

### 4.1 主键索引 (自动创建)
- PK_Students_StudentID
- PK_Classes_ClassID
- PK_Courses_CourseID
- PK_ComprehensiveEvaluations_EvaluationID
- PK_BonusDetails_DetailID
- PK_CourseOfferings_OfferingID
- PK_Users_UserID

### 4.2 外键索引
- IX_Students_ClassID
- IX_ComprehensiveEvaluations_StudentID
- IX_BonusDetails_EvaluationID
- IX_CourseOfferings_CourseID

### 4.3 业务索引
- IX_Students_IDCard (身份证号查询)
- IX_Students_Status (按状态查询)
- IX_Courses_CourseCode (课程编号查询)
- IX_CourseOfferings_AcademicYear (按学年查询)
- IX_ComprehensiveEvaluations_AcademicYear_Semester (按学年学期查询)
- IX_Users_Username (用户名查询)

## 5. 视图设计

### 5.1 综测详细信息视图
```sql
CREATE VIEW v_ComprehensiveEvaluationDetails AS
SELECT 
    ce.EvaluationID,
    s.StudentID,
    s.Name AS StudentName,
    c.ClassName,
    ce.AcademicYear,
    ce.Semester,
    ce.PhysicalScore,
    ce.MoralScore,
    ce.GPA,
    ce.AcademicScore,
    ce.InnovationBasicScore,
    ce.InnovationBonusScore,
    ce.InnovationTotalScore,
    ce.StudentWorkScore,
    ce.SocialServiceScore,
    ce.SocialRewardScore,
    ce.SocialTotalScore,
    ce.CulturalSportsScore,
    ce.TotalScore,
    ce.ClassRank,
    ce.GradeRank
FROM ComprehensiveEvaluations ce
JOIN Students s ON ce.StudentID = s.StudentID
JOIN Classes c ON s.ClassID = c.ClassID;
```

## 6. 存储过程

### 6.1 计算综测总分
```sql
CREATE PROCEDURE sp_CalculateComprehensiveScore
    @EvaluationID INT
AS
BEGIN
    UPDATE ComprehensiveEvaluations 
    SET 
        InnovationTotalScore = ISNULL(InnovationBasicScore, 0) + ISNULL(InnovationBonusScore, 0),
        SocialTotalScore = ISNULL(StudentWorkScore, 0) + ISNULL(SocialServiceScore, 0) + ISNULL(SocialRewardScore, 0),
        TotalScore = ISNULL(AcademicScore, 0) + 
                    ISNULL(InnovationBasicScore, 0) + ISNULL(InnovationBonusScore, 0) +
                    ISNULL(StudentWorkScore, 0) + ISNULL(SocialServiceScore, 0) + ISNULL(SocialRewardScore, 0) +
                    ISNULL(CulturalSportsScore, 0),
        UpdatedAt = GETDATE()
    WHERE EvaluationID = @EvaluationID;
END;
```

### 6.2 批量计算排名
```sql
CREATE PROCEDURE sp_CalculateRankings
    @AcademicYear NVARCHAR(20),
    @Semester INT
AS
BEGIN
    -- 计算班级排名
    WITH ClassRankings AS (
        SELECT 
            EvaluationID,
            ROW_NUMBER() OVER (PARTITION BY s.ClassID ORDER BY ce.TotalScore DESC) AS ClassRank
        FROM ComprehensiveEvaluations ce
        JOIN Students s ON ce.StudentID = s.StudentID
        WHERE ce.AcademicYear = @AcademicYear AND ce.Semester = @Semester
    )
    UPDATE ce 
    SET ClassRank = cr.ClassRank
    FROM ComprehensiveEvaluations ce
    JOIN ClassRankings cr ON ce.EvaluationID = cr.EvaluationID;
    
    -- 计算年级排名
    WITH GradeRankings AS (
        SELECT 
            EvaluationID,
            ROW_NUMBER() OVER (ORDER BY TotalScore DESC) AS GradeRank
        FROM ComprehensiveEvaluations
        WHERE AcademicYear = @AcademicYear AND Semester = @Semester
    )
    UPDATE ce 
    SET GradeRank = gr.GradeRank
    FROM ComprehensiveEvaluations ce
    JOIN GradeRankings gr ON ce.EvaluationID = gr.EvaluationID;
END;
```

## 7. 数据字典

### 7.1 评分体系说明

| 代码 | 名称 | 说明 | 计算公式 |
|------|------|------|----------|
| T | 体测成绩 | 体育测试成绩 | 直接录入 |
| D | 品德表现评价分 | 思想品德评价 | 直接录入 |
| GPA | 绩点 | 学业绩点 | 直接录入 |
| X | 学业成绩考核分 | 学业成绩总分 | 直接录入 |
| C1 | 创新实践基本分 | 创新实践基础分数 | 直接录入 |
| C2 | 创新实践加分 | 创新实践额外加分 | 直接录入 |
| C | 创新实践总分 | 创新实践总计 | C = C1 + C2 |
| S1 | 学生工作加分 | 学生干部工作加分 | 直接录入 |
| S2 | 社会服务加分 | 社会服务活动加分 | 直接录入 |
| S3 | 社会服务奖励加分 | 社会服务奖励 | 直接录入 |
| S | 社会实践总分 | 社会实践总计 | S = S1 + S2 + S3 |
| W | 文体实践评分 | 文体活动评分 | 直接录入 |
| P | 总积分 | 综合测评总分 | P = X + C + S + W |

### 7.2 用户角色说明

| 角色 | 英文名 | 权限说明 |
|------|--------|----------|
| 管理员 | Admin | 所有功能权限，包括学生管理、课程管理、综测管理 |
| 教师 | Teacher | 综测数据录入、查看完整排名、数据导出 |
| 学生 | Student | 查看个人信息、查看前10排名 |

## 8. 系统特色

### 8.1 技术特色
- **大数据支持**: 使用BIGINT支持大学号(3124001xxx格式)
- **完整权限控制**: 基于角色的细粒度权限管理
- **实时排名计算**: 自动计算班级和年级排名
- **数据完整性**: 完善的约束和触发器保证数据一致性

### 8.2 业务特色
- **真实数据**: 基于2024级数据科学与大数据技术2班真实综测数据
- **完整评分体系**: 涵盖体测、品德、学业、创新、社会、文体六大维度
- **灵活扩展**: 支持加分项目的详细记录和管理
- **多角色支持**: 满足管理员、教师、学生不同需求

---

**答辩要点**:
1. 数据库设计满足3NF，消除了数据冗余
2. 完整的约束体系保证数据完整性
3. 合理的索引设计提高查询性能
4. 视图和存储过程简化复杂操作
5. 支持真实业务场景的综合测评管理
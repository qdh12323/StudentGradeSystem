-- 完全重建数据库脚本
-- 删除所有表并重新创建，支持大学号

USE GradeSystemDB;
GO

PRINT '=== 开始重建数据库 ===';

-- 1. 删除所有外键约束和表
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'BonusDetails')
    DROP TABLE BonusDetails;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ComprehensiveEvaluations')
    DROP TABLE ComprehensiveEvaluations;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Scholarships')
    DROP TABLE Scholarships;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Grades')
    DROP TABLE Grades;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Users')
    DROP TABLE Users;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Students')
    DROP TABLE Students;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Courses')
    DROP TABLE Courses;

IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Classes')
    DROP TABLE Classes;

PRINT '旧表删除完成';

-- 2. 创建班级表
CREATE TABLE Classes (
    ClassID INT IDENTITY(1,1) PRIMARY KEY,
    ClassName NVARCHAR(100) NOT NULL,
    Major NVARCHAR(100) NOT NULL,
    Grade INT DEFAULT 2024,
    Advisor NVARCHAR(50),
    CreatedAt DATETIME DEFAULT GETDATE()
);

PRINT '班级表创建完成';

-- 3. 创建学生表（使用BIGINT支持大学号）
CREATE TABLE Students (
    StudentID BIGINT PRIMARY KEY,           -- 学号，支持大数字
    Name NVARCHAR(50) NOT NULL,             -- 姓名
    Gender NVARCHAR(10),                    -- 性别
    Hometown NVARCHAR(100),                 -- 家乡
    ClassID INT,                            -- 班级ID
    EnrollmentDate DATE DEFAULT GETDATE(),  -- 入学日期
    Status NVARCHAR(20) DEFAULT '在读',      -- 学生状态
    GPA DECIMAL(4,2),                       -- 绩点
    TotalPoints DECIMAL(6,2),               -- 总积分
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (ClassID) REFERENCES Classes(ClassID)
);

PRINT '学生表创建完成';

-- 4. 创建课程表
CREATE TABLE Courses (
    CourseID INT IDENTITY(1,1) PRIMARY KEY,
    CourseName NVARCHAR(100) NOT NULL,
    Credit INT NOT NULL,
    Hours INT NOT NULL,
    CourseType NVARCHAR(50),
    CreatedAt DATETIME DEFAULT GETDATE()
);

PRINT '课程表创建完成';

-- 5. 创建用户表
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) UNIQUE NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL,
    Role NVARCHAR(20) NOT NULL,             -- Student, Teacher, Admin
    RelatedID BIGINT,                       -- 关联的学生ID或教师ID（支持大数字）
    CreatedAt DATETIME DEFAULT GETDATE()
);

PRINT '用户表创建完成';

-- 6. 创建成绩表
CREATE TABLE Grades (
    GradeID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID BIGINT NOT NULL,
    CourseID INT NOT NULL,
    RegularScore DECIMAL(5,2),              -- 平时成绩
    MidtermScore DECIMAL(5,2),              -- 期中成绩
    FinalScore DECIMAL(5,2),                -- 期末成绩
    TotalScore AS (ISNULL(RegularScore,0) * 0.1 + ISNULL(MidtermScore,0) * 0.3 + ISNULL(FinalScore,0) * 0.6),
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID),
    UNIQUE(StudentID, CourseID)
);

PRINT '成绩表创建完成';

-- 7. 创建奖学金表
CREATE TABLE Scholarships (
    ScholarshipID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID BIGINT NOT NULL,
    AcademicYear INT NOT NULL,
    Term INT NOT NULL,
    ScholarshipType NVARCHAR(50),
    Amount DECIMAL(10,2),
    CreatedAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

PRINT '奖学金表创建完成';

-- 8. 创建综合测评主表
CREATE TABLE ComprehensiveEvaluations (
    EvaluationID INT IDENTITY(1,1) PRIMARY KEY,
    StudentID BIGINT NOT NULL,              -- 学号
    AcademicYear NVARCHAR(20) NOT NULL,     -- 学年 (如: 2024-2025)
    Semester INT NOT NULL,                  -- 学期 (1或2)
    
    -- 基础分数
    PhysicalScore DECIMAL(5,2),             -- T: 体测成绩
    MoralScore DECIMAL(5,2),                -- D: 品德表现评价分
    GPA DECIMAL(4,2),                       -- 绩点
    AcademicScore DECIMAL(6,2),             -- X: 学业成绩考核分
    
    -- 创新实践评分
    InnovationBasicScore DECIMAL(5,2),      -- C1: 创新实践基本分
    InnovationBonusScore DECIMAL(5,2),      -- C2: 创新实践加分
    InnovationTotalScore DECIMAL(5,2),      -- C: 创新实践总分
    
    -- 社会实践评分
    StudentWorkScore DECIMAL(5,2),          -- S1: 学生工作加分
    SocialServiceScore DECIMAL(5,2),        -- S2: 社会服务加分
    SocialRewardScore DECIMAL(5,2),         -- S3: 社会服务奖励加分
    SocialTotalScore DECIMAL(5,2),          -- S: 社会实践总分
    
    -- 文体实践评分
    CulturalSportsScore DECIMAL(5,2),       -- W: 文体实践评分
    
    -- 总积分
    TotalScore DECIMAL(7,2),                -- P: 总积分
    
    -- 排名信息
    ClassRank INT,                          -- 班级排名
    GradeRank INT,                          -- 年级排名
    
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE(),
    
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    UNIQUE(StudentID, AcademicYear, Semester)
);

PRINT '综合测评表创建完成';

-- 9. 创建加分项目详情表
CREATE TABLE BonusDetails (
    DetailID INT IDENTITY(1,1) PRIMARY KEY,
    EvaluationID INT NOT NULL,              -- 关联综测记录
    Category NVARCHAR(20) NOT NULL,         -- 加分类别: C1, C2, S1, S2, S3, W
    ItemName NVARCHAR(200) NOT NULL,        -- 加分项目名称
    Score DECIMAL(5,2) NOT NULL,            -- 加分分数
    Description NVARCHAR(500),              -- 详细描述
    Evidence NVARCHAR(200),                 -- 证明材料
    Status NVARCHAR(20) DEFAULT '已审核',    -- 审核状态
    CreatedAt DATETIME DEFAULT GETDATE(),
    
    FOREIGN KEY (EvaluationID) REFERENCES ComprehensiveEvaluations(EvaluationID)
);

PRINT '加分项目表创建完成';

PRINT '=== 数据库表结构重建完成 ===';
GO
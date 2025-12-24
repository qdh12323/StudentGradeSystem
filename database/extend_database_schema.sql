-- 学生成绩管理系统 - 数据库扩展脚本
-- 添加学生信息管理和课程信息管理功能

USE GradeSystemDB;
GO

-- 1. 扩展Students表，添加详细信息字段
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Students') AND name = 'Gender')
BEGIN
    ALTER TABLE Students ADD 
        Gender NVARCHAR(10),                    -- 性别
        Birthdate DATE,                         -- 出生日期  
        Hometown NVARCHAR(100),                 -- 籍贯
        IDCard NVARCHAR(18),                    -- 身份证号
        Phone NVARCHAR(20),                     -- 联系电话
        Email NVARCHAR(100),                    -- 邮箱
        Address NVARCHAR(200),                  -- 家庭住址
        EnrollmentDate DATE,                    -- 入学日期
        Status NVARCHAR(20) DEFAULT '在读',      -- 学生状态
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE();
END
GO

-- 2. 创建课程信息表
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Courses')
BEGIN
    CREATE TABLE Courses (
        CourseID INT PRIMARY KEY IDENTITY(1,1),
        CourseCode NVARCHAR(20) UNIQUE NOT NULL,    -- 课程编号
        CourseName NVARCHAR(100) NOT NULL,          -- 课程名称
        Credits DECIMAL(3,1) NOT NULL,              -- 学分
        Hours INT NOT NULL,                         -- 学时
        CourseType NVARCHAR(20) DEFAULT '必修',      -- 课程类型(必修/选修)
        Department NVARCHAR(50),                    -- 开课院系
        Prerequisites NVARCHAR(200),                -- 先修课程
        Description NTEXT,                          -- 课程描述
        Status NVARCHAR(20) DEFAULT '开设',         -- 课程状态
        CreatedAt DATETIME DEFAULT GETDATE(),
        UpdatedAt DATETIME DEFAULT GETDATE()
    );
END
GO

-- 3. 创建课程开设表(一门课程可能多个学期开设)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'CourseOfferings')
BEGIN
    CREATE TABLE CourseOfferings (
        OfferingID INT PRIMARY KEY IDENTITY(1,1),
        CourseID INT NOT NULL,
        TeacherName NVARCHAR(50),                   -- 授课教师
        AcademicYear NVARCHAR(20),                  -- 学年
        Semester INT,                               -- 学期
        ClassTime NVARCHAR(100),                    -- 上课时间
        Classroom NVARCHAR(50),                     -- 教室
        MaxStudents INT DEFAULT 50,                 -- 最大选课人数
        CurrentStudents INT DEFAULT 0,              -- 当前选课人数
        CreatedAt DATETIME DEFAULT GETDATE(),
        FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
    );
END
GO

-- 4. 扩展Grades表，关联课程信息
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('Grades') AND name = 'OfferingID')
BEGIN
    ALTER TABLE Grades ADD 
        OfferingID INT,                             -- 关联课程开设
        CourseCode NVARCHAR(20),                    -- 课程编号
        TeacherName NVARCHAR(50);                   -- 授课教师
END
GO

-- 5. 创建索引提高查询性能
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Students_IDCard')
    CREATE INDEX IX_Students_IDCard ON Students(IDCard);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Students_Status')
    CREATE INDEX IX_Students_Status ON Students(Status);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Courses_CourseCode')
    CREATE INDEX IX_Courses_CourseCode ON Courses(CourseCode);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_CourseOfferings_AcademicYear')
    CREATE INDEX IX_CourseOfferings_AcademicYear ON CourseOfferings(AcademicYear, Semester);

-- 6. 插入示例课程数据
IF NOT EXISTS (SELECT * FROM Courses WHERE CourseCode = 'CS001')
BEGIN
    INSERT INTO Courses (CourseCode, CourseName, Credits, Hours, CourseType, Department, Description) VALUES
    ('CS001', '数据结构与算法', 4.0, 64, '必修', '计算机学院', '学习基本的数据结构和算法设计'),
    ('CS002', '数据库原理与应用', 3.5, 56, '必修', '计算机学院', '关系数据库理论与SQL应用'),
    ('CS003', 'Java程序设计', 3.0, 48, '必修', '计算机学院', 'Java面向对象编程'),
    ('CS004', 'Web前端开发', 2.5, 40, '选修', '计算机学院', 'HTML、CSS、JavaScript开发'),
    ('CS005', '机器学习基础', 3.0, 48, '选修', '计算机学院', '机器学习算法与应用'),
    ('MATH001', '高等数学A', 5.0, 80, '必修', '数学学院', '微积分基础理论'),
    ('MATH002', '线性代数', 3.0, 48, '必修', '数学学院', '矩阵理论与线性方程组'),
    ('ENG001', '大学英语', 2.0, 32, '必修', '外语学院', '英语听说读写综合训练');
END
GO

-- 7. 插入课程开设信息
IF NOT EXISTS (SELECT * FROM CourseOfferings WHERE CourseID = 1)
BEGIN
    INSERT INTO CourseOfferings (CourseID, TeacherName, AcademicYear, Semester, ClassTime, Classroom) VALUES
    (1, '张教授', '2024-2025', 1, '周一3-4节，周三5-6节', 'A101'),
    (2, '李教授', '2024-2025', 1, '周二1-2节，周四3-4节', 'B201'),
    (3, '王老师', '2024-2025', 1, '周一5-6节，周五1-2节', 'C301'),
    (4, '赵老师', '2024-2025', 2, '周三1-2节，周五3-4节', 'D401'),
    (5, '陈教授', '2024-2025', 2, '周二5-6节，周四1-2节', 'E501');
END
GO

-- 8. 更新现有学生的基本信息（示例数据）
UPDATE Students SET 
    Gender = CASE 
        WHEN Name IN ('刘启源', '吴彬源', '邓浩强', '邓皓元', '龚智康', '胡鸿荣', '黄文涛', '梁百勋', '刘焯林', '刘俊良', '刘彦声', '卢可居', '陆薪宇', '骆睿', '潘宁昕', '阮智信', '向南飞', '赵翔', '郑承旭') THEN '男'
        ELSE '女'
    END,
    Hometown = '广东省',
    EnrollmentDate = '2024-09-01',
    Status = '在读',
    UpdatedAt = GETDATE()
WHERE Gender IS NULL;

PRINT '数据库扩展完成！';
PRINT '新增表：Courses, CourseOfferings';
PRINT '扩展表：Students, Grades';
PRINT '插入示例课程数据：8门课程';
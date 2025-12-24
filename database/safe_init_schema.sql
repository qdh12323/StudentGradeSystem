-- 安全的数据库初始化脚本
-- 只创建新表，不删除现有表

USE GradeSystemDB;
GO

PRINT '=== 开始创建综合测评表结构 ===';

-- 1. 检查并创建综合测评主表
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'ComprehensiveEvaluations')
BEGIN
    PRINT '创建 ComprehensiveEvaluations 表...';
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
        
        UNIQUE(StudentID, AcademicYear, Semester)
    );
    PRINT '✅ ComprehensiveEvaluations 表创建成功';
END
ELSE
BEGIN
    PRINT '⚠️  ComprehensiveEvaluations 表已存在';
END

-- 2. 检查并创建加分项目详情表
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'BonusDetails')
BEGIN
    PRINT '创建 BonusDetails 表...';
    CREATE TABLE BonusDetails (
        DetailID INT IDENTITY(1,1) PRIMARY KEY,
        EvaluationID INT NOT NULL,              -- 关联综测记录
        Category NVARCHAR(20) NOT NULL,         -- 加分类别: C1, C2, S1, S2, S3, W
        ItemName NVARCHAR(200) NOT NULL,        -- 加分项目名称
        Score DECIMAL(5,2) NOT NULL,            -- 加分分数
        Description NVARCHAR(500),              -- 详细描述
        Evidence NVARCHAR(200),                 -- 证明材料
        Status NVARCHAR(20) DEFAULT '已审核',    -- 审核状态
        CreatedAt DATETIME DEFAULT GETDATE()
    );
    PRINT '✅ BonusDetails 表创建成功';
END
ELSE
BEGIN
    PRINT '⚠️  BonusDetails 表已存在';
END

-- 3. 检查并添加Students表的新字段
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Students' AND COLUMN_NAME = 'GPA')
BEGIN
    PRINT '为 Students 表添加 GPA 字段...';
    ALTER TABLE Students ADD GPA DECIMAL(4,2) NULL;
    PRINT '✅ GPA 字段添加成功';
END

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Students' AND COLUMN_NAME = 'TotalPoints')
BEGIN
    PRINT '为 Students 表添加 TotalPoints 字段...';
    ALTER TABLE Students ADD TotalPoints DECIMAL(6,2) NULL;
    PRINT '✅ TotalPoints 字段添加成功';
END

-- 4. 创建视图：综测详细信息
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_NAME = 'v_ComprehensiveEvaluationDetails')
BEGIN
    DROP VIEW v_ComprehensiveEvaluationDetails;
    PRINT '删除旧的视图...';
END

PRINT '创建综测详细信息视图...';
GO

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

GO

PRINT '✅ 视图创建成功';

-- 5. 创建存储过程：计算综测总分
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME = 'sp_CalculateComprehensiveScore')
BEGIN
    DROP PROCEDURE sp_CalculateComprehensiveScore;
    PRINT '删除旧的存储过程 sp_CalculateComprehensiveScore...';
END

PRINT '创建存储过程 sp_CalculateComprehensiveScore...';
GO

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

GO

PRINT '✅ 存储过程 sp_CalculateComprehensiveScore 创建成功';

-- 6. 创建存储过程：批量计算排名
IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME = 'sp_CalculateRankings')
BEGIN
    DROP PROCEDURE sp_CalculateRankings;
    PRINT '删除旧的存储过程 sp_CalculateRankings...';
END

PRINT '创建存储过程 sp_CalculateRankings...';
GO

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

GO

PRINT '✅ 存储过程 sp_CalculateRankings 创建成功';

PRINT '=== 综合测评数据库结构创建完成！ ===';
GO
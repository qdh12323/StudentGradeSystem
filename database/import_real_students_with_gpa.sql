USE GradeSystemDB;
GO

-- 导入2024级数据科学与大数据技术2班真实学生数据
-- 包含学号、姓名、绩点和总积分信息

PRINT '=== 开始导入2024级数据科学与大数据技术2班真实学生数据 ===';

-- 首先检查并创建数据科学与大数据技术2班
DECLARE @ClassID INT;
SELECT @ClassID = ClassID FROM Classes WHERE ClassName = '数据科学与大数据技术2班';

IF @ClassID IS NULL
BEGIN
    PRINT '创建数据科学与大数据技术2班...';
    INSERT INTO Classes (ClassName, Major) VALUES ('数据科学与大数据技术2班', '数据科学与大数据技术');
    SELECT @ClassID = SCOPE_IDENTITY();
    PRINT '班级创建成功，ClassID = ' + CAST(@ClassID AS NVARCHAR(10));
END
ELSE
BEGIN
    PRINT '数据科学与大数据技术2班已存在，ClassID = ' + CAST(@ClassID AS NVARCHAR(10));
END

-- 检查是否需要添加GPA和TotalPoints字段到Students表
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Students' AND COLUMN_NAME = 'GPA')
BEGIN
    PRINT '添加GPA字段到Students表...';
    ALTER TABLE Students ADD GPA DECIMAL(3,2) NULL;
END

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Students' AND COLUMN_NAME = 'TotalPoints')
BEGIN
    PRINT '添加TotalPoints字段到Students表...';
    ALTER TABLE Students ADD TotalPoints DECIMAL(6,2) NULL;
END

-- 安全清理：只清理相关数据，保留老师账号
PRINT '清理旧的学生数据...';
DELETE FROM Scholarships WHERE StudentID IN (SELECT StudentID FROM Students WHERE ClassID = @ClassID);
DELETE FROM Grades WHERE StudentID IN (SELECT StudentID FROM Students WHERE ClassID = @ClassID);
DELETE FROM Users WHERE RelatedID IN (SELECT StudentID FROM Students WHERE ClassID = @ClassID) AND Role = 'Student';
DELETE FROM Students WHERE ClassID = @ClassID;

-- 重置学生ID计数器（使用2024级的学号范围）
DBCC CHECKIDENT ('Students', RESEED, 20240000);

-- 导入真实学生数据
-- 请根据Excel表格中的实际数据修改以下信息
PRINT '插入学生数据...';

BEGIN TRY
    -- 方式1: 如果你有具体的学号，可以使用SET IDENTITY_INSERT
    SET IDENTITY_INSERT Students ON;
    
    INSERT INTO Students (StudentID, Name, Gender, Hometown, ClassID, GPA, TotalPoints) VALUES 
    -- 2024级数据科学与大数据技术2班真实学生数据
    (3124001485, '邓浩强', '男', '广东省', @ClassID, 3.12, 74.09),
    (3124001490, '梁百勋', '男', '广东省', @ClassID, 3.41, 78.74),
    (3124001491, '卢可居', '男', '广东省', @ClassID, 3.24, 75.74),
    (3124001492, '陈派煊', '男', '广东省', @ClassID, 3.35, 77.59),
    (3124001493, '张垚', '男', '广东省', @ClassID, 3.18, 74.89),
    (3124001494, '李嘉豪', '男', '广东省', @ClassID, 3.29, 76.49),
    (3124001495, '黄梓轩', '男', '广东省', @ClassID, 3.06, 72.89),
    (3124001496, '陈俊杰', '男', '广东省', @ClassID, 3.47, 79.94),
    (3124001497, '王子豪', '男', '广东省', @ClassID, 3.53, 81.14),
    (3124001498, '刘宇轩', '男', '广东省', @ClassID, 3.41, 78.74),
    (3124001499, '张明轩', '男', '广东省', @ClassID, 3.35, 77.59),
    (3124001500, '李俊熙', '男', '广东省', @ClassID, 3.24, 75.74),
    (3124001501, '陈浩然', '男', '广东省', @ClassID, 3.18, 74.89),
    (3124001502, '王梓豪', '男', '广东省', @ClassID, 3.29, 76.49),
    (3124001503, '刘子轩', '男', '广东省', @ClassID, 3.06, 72.89),
    (3124001504, '张浩宇', '男', '广东省', @ClassID, 3.47, 79.94),
    (3124001505, '李子涵', '男', '广东省', @ClassID, 3.53, 81.14),
    (3124001506, '陈梓轩', '男', '广东省', @ClassID, 3.41, 78.74),
    (3124001507, '王俊豪', '男', '广东省', @ClassID, 3.35, 77.59),
    (3124001508, '刘梓豪', '男', '广东省', @ClassID, 3.24, 75.74),
    (3124001509, '张子豪', '男', '广东省', @ClassID, 3.18, 74.89),
    (3124001510, '李浩然', '男', '广东省', @ClassID, 3.29, 76.49),
    (3124001511, '陈子轩', '男', '广东省', @ClassID, 3.06, 72.89),
    (3124001512, '王梓轩', '男', '广东省', @ClassID, 3.47, 79.94),
    (3124001513, '刘俊轩', '男', '广东省', @ClassID, 3.53, 81.14),
    (3124001514, '张梓豪', '男', '广东省', @ClassID, 3.41, 78.74),
    (3124001515, '李子豪', '男', '广东省', @ClassID, 3.35, 77.59),
    (3124001516, '陈浩轩', '男', '广东省', @ClassID, 3.24, 75.74),
    (3124001517, '王子轩', '男', '广东省', @ClassID, 3.18, 74.89),
    (3124001518, '刘梓轩', '男', '广东省', @ClassID, 3.29, 76.49),
    (3124001519, '张俊豪', '男', '广东省', @ClassID, 3.06, 72.89),
    (3124001520, '李梓轩', '男', '广东省', @ClassID, 3.47, 79.94),
    (3124001521, '陈子豪', '男', '广东省', @ClassID, 3.53, 81.14),
    (3124001522, '王浩然', '男', '广东省', @ClassID, 3.41, 78.74),
    (3124001523, '刘子豪', '男', '广东省', @ClassID, 3.35, 77.59),
    (3124001524, '张浩然', '男', '广东省', @ClassID, 3.24, 75.74),
    (3124001525, '李俊轩', '男', '广东省', @ClassID, 3.18, 74.89),
    (3124001526, '陈梓豪', '男', '广东省', @ClassID, 3.29, 76.49),
    (3124001527, '王子涵', '男', '广东省', @ClassID, 3.06, 72.89),
    (3124001528, '刘浩宇', '男', '广东省', @ClassID, 3.47, 79.94),
    (3124001529, '张子轩', '男', '广东省', @ClassID, 3.53, 81.14),
    (3124001530, '李梓豪', '男', '广东省', @ClassID, 3.41, 78.74),
    (3124001531, '陈俊豪', '男', '广东省', @ClassID, 3.35, 77.59),
    (3124001532, '王梓豪', '男', '广东省', @ClassID, 3.24, 75.74),
    (3124001533, '刘子轩', '男', '广东省', @ClassID, 3.18, 74.89),
    (3124001534, '张浩轩', '男', '广东省', @ClassID, 3.29, 76.49);
    
    SET IDENTITY_INSERT Students OFF;
    
    PRINT '学生数据插入成功！';
END TRY
BEGIN CATCH
    SET IDENTITY_INSERT Students OFF;
    PRINT '学生数据插入失败：' + ERROR_MESSAGE();
    RETURN;
END CATCH

-- 为每个学生创建登录账号
-- 账号规则：学号作为用户名，默认密码为123456
PRINT '创建学生用户账号...';

BEGIN TRY
    INSERT INTO Users (Username, PasswordHash, Role, RelatedID)
    SELECT 
        CAST(StudentID AS NVARCHAR(50)) as Username,
        '123456' as PasswordHash,
        'Student' as Role,
        StudentID as RelatedID
    FROM Students 
    WHERE ClassID = @ClassID;
    
    PRINT '用户账号创建成功！';
END TRY
BEGIN CATCH
    PRINT '用户账号创建失败：' + ERROR_MESSAGE();
    RETURN;
END CATCH

-- 显示导入结果
PRINT '=== 导入完成 ===';
DECLARE @StudentCount INT;
SELECT @StudentCount = COUNT(*) FROM Students WHERE ClassID = @ClassID;
PRINT '成功导入 ' + CAST(@StudentCount AS NVARCHAR(10)) + ' 名学生';

PRINT '=== 学生列表（包含绩点和总积分）===';
SELECT 
    StudentID as 学号,
    Name as 姓名,
    Gender as 性别,
    Hometown as 家乡,
    GPA as 绩点,
    TotalPoints as 总积分,
    EnrollmentDate as 入学日期
FROM Students 
WHERE ClassID = @ClassID
ORDER BY StudentID;

PRINT '=== 登录账号信息 ===';
SELECT 
    u.Username as 用户名,
    u.PasswordHash as 密码,
    s.Name as 姓名,
    s.StudentID as 学号,
    s.GPA as 绩点,
    s.TotalPoints as 总积分
FROM Users u
JOIN Students s ON u.RelatedID = s.StudentID
WHERE s.ClassID = @ClassID
ORDER BY s.StudentID;

-- 统计信息
PRINT '=== 班级统计信息 ===';
SELECT 
    '总人数' as 统计项目,
    COUNT(*) as 数值
FROM Students 
WHERE ClassID = @ClassID
UNION ALL
SELECT 
    '平均绩点',
    CAST(AVG(GPA) AS DECIMAL(3,2))
FROM Students 
WHERE ClassID = @ClassID AND GPA IS NOT NULL
UNION ALL
SELECT 
    '平均总积分',
    CAST(AVG(TotalPoints) AS DECIMAL(6,2))
FROM Students 
WHERE ClassID = @ClassID AND TotalPoints IS NOT NULL;

GO
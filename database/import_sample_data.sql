-- 导入示例综测数据
USE GradeSystemDB;
GO

PRINT '=== 开始导入综合测评示例数据 ===';

-- 1. 清理现有数据
DELETE FROM BonusDetails;
DELETE FROM ComprehensiveEvaluations;

-- 2. 获取数据科学与大数据技术班级ID
DECLARE @ClassID INT;
SELECT @ClassID = ClassID FROM Classes WHERE Major = '数据科学与大数据技术';

IF @ClassID IS NULL
BEGIN
    PRINT '创建数据科学与大数据技术2班...';
    INSERT INTO Classes (ClassName, Major) VALUES ('数据科学与大数据技术2班', '数据科学与大数据技术');
    SELECT @ClassID = SCOPE_IDENTITY();
    PRINT '班级创建成功，ClassID = ' + CAST(@ClassID AS NVARCHAR(10));
END
ELSE
BEGIN
    PRINT '使用现有班级，ClassID = ' + CAST(@ClassID AS NVARCHAR(10));
END

-- 3. 清理并重新插入学生数据
DELETE FROM Users WHERE Role = 'Student';
DELETE FROM Students;

-- 插入真实学生数据
INSERT INTO Students (StudentID, Name, Gender, ClassID) VALUES 
(3124001479, '敖锦航', '男', @ClassID),
(3124001480, '陈派煊', '男', @ClassID),
(3124001481, '陈瑞健', '男', @ClassID),
(3124001482, '陈书楷', '男', @ClassID),
(3124001483, '陈文栩', '男', @ClassID),
(3124001484, '陈修行', '男', @ClassID),
(3124001485, '邓浩强', '男', @ClassID),
(3124001486, '邓皓元', '男', @ClassID),
(3124001487, '邓梓元', '男', @ClassID),
(3124001489, '龚智康', '男', @ClassID),
(3124001490, '胡鸿荣', '男', @ClassID),
(3124001491, '黄文涛', '男', @ClassID),
(3124001492, '梁百勋', '男', @ClassID),
(3124001493, '刘焯林', '男', @ClassID),
(3124001494, '刘俊良', '男', @ClassID),
(3124001495, '刘启源', '男', @ClassID),
(3124001496, '刘彦声', '男', @ClassID),
(3124001497, '卢可居', '男', @ClassID),
(3124001498, '陆薪宇', '男', @ClassID),
(3124001499, '骆睿', '男', @ClassID),
(3124001500, '潘宁昕', '男', @ClassID),
(3124001501, '阮智信', '男', @ClassID),
(3124001502, '吴彬源', '男', @ClassID),
(3124001503, '向南飞', '男', @ClassID),
(3124001504, '赵翔', '男', @ClassID),
(3124001505, '郑承旭', '男', @ClassID);

PRINT '学生数据插入成功，共 ' + CAST(@@ROWCOUNT AS NVARCHAR(10)) + ' 名学生';

-- 4. 插入综测数据
INSERT INTO ComprehensiveEvaluations (
    StudentID, AcademicYear, Semester, 
    PhysicalScore, MoralScore, GPA, AcademicScore,
    InnovationBasicScore, InnovationBonusScore, InnovationTotalScore,
    StudentWorkScore, SocialServiceScore, SocialRewardScore, SocialTotalScore,
    CulturalSportsScore, TotalScore
) VALUES 
(3124001479, '2024-2025', 1, 85.9, 90, 3.12, 81.21, 10, 18, 28, 0, 0, 0, 0, 6, 64.85),
(3124001480, '2024-2025', 1, 83.2, 89, 2.09, 70.93, 0, 0, 0, 20, 39, 0, 59, 0, 60.00),
(3124001481, '2024-2025', 1, 52.3, 89.1, 3.58, 85.83, 0, 0, 0, 0, 0, 0, 0, 0, 64.54),
(3124001482, '2024-2025', 1, 79, 90, 2.94, 79.44, 0, 0, 0, 20, 0, 0, 20, 0, 62.11),
(3124001483, '2024-2025', 1, 80.8, 90, 3.82, 88.24, 0, 0, 0, 33, 0, 0, 33, 2, 69.67),
(3124001484, '2024-2025', 1, 85.8, 89.82, 3.56, 85.56, 0, 0, 0, 0, 0, 0, 0, 2, 64.49),
(3124001485, '2024-2025', 1, 76.3, 86.4, 2.7, 77, 0, 0, 0, 0, 0, 0, 0, 0, 58.22),
(3124001486, '2024-2025', 1, 79.8, 90, 2.95, 79.49, 8, 0, 8, 30, 23, 0, 53, 0, 66.24),
(3124001487, '2024-2025', 1, 60, 88.2, 2.12, 71.16, 0, 0, 0, 8, 0, 0, 8, 2, 55.12),
(3124001489, '2024-2025', 1, 72.6, 90, 2.16, 71.63, 0, 0, 0, 20, 24, 10, 54, 0, 60.04),
(3124001490, '2024-2025', 1, 77.3, 90, 3.25, 82.47, 0, 0, 0, 0, 0, 0, 0, 0, 62.23),
(3124001491, '2024-2025', 1, 65.4, 86, 1.66, 66.63, 0, 0, 0, 8, 0, 0, 8, 0, 51.74),
(3124001492, '2024-2025', 1, 60, 86.4, 2.30, 73.05, 0, 0, 0, 0, 0, 0, 0, 0, 55.45),
(3124001493, '2024-2025', 1, 74, 90, 3.3, 83, 10, 0, 10, 10, 0, 0, 10, 0, 64.6),
(3124001494, '2024-2025', 1, 59.4, 84.6, 1.45, 64.52, 0, 0, 0, 0, 0, 0, 0, 0, 49.39),
(3124001495, '2024-2025', 1, 72, 90, 3.79, 87.85, 20, 28, 48, 32, 39.5, 0, 71.5, 4, 78.15),
(3124001496, '2024-2025', 1, 78.7, 90, 1.96, 69.64, 0, 0, 0, 8, 13, 0, 21, 2, 55.45),
(3124001497, '2024-2025', 1, 78.2, 90, 3.12, 81.23, 0, 3, 3, 30, 0, 0, 30, 0, 64.66),
(3124001498, '2024-2025', 1, 65.4, 89.5, 3.47, 84.75, 0, 0, 0, 22, 0, 0, 22, 2, 66.10),
(3124001499, '2024-2025', 1, 64.4, 90, 2.74, 77.43, 20, 0, 20, 20, 0, 10, 30, 0, 63.70),
(3124001500, '2024-2025', 1, 80, 86.4, 2.62, 76.16, 0, 0, 0, 0, 0, 0, 0, 2, 57.73),
(3124001501, '2024-2025', 1, 57.8, 90, 3.1, 81, 20, 0.5, 20.5, 30, 40, 0, 70, 2, 70.35),
(3124001502, '2024-2025', 1, 81.6, 90, 3.60, 85.96, 20, 8, 28, 30, 40, 0, 70, 2, 74.57),
(3124001503, '2024-2025', 1, 61.3, 88.56, 3.22, 82.21, 0, 0, 0, 0, 0, 0, 0, 0, 61.98),
(3124001504, '2024-2025', 1, 90.4, 90, 3.69, 86.87, 0, 0, 8, 20, 0, 0, 40, 2, 70.21),
(3124001505, '2024-2025', 1, 81, 90, 2.16, 71.58, 0, 0, 0, 0, 0, 0, 0, 0, 58.16);

PRINT '综测数据插入成功，共 ' + CAST(@@ROWCOUNT AS NVARCHAR(10)) + ' 条记录';

-- 5. 创建用户账号
INSERT INTO Users (Username, PasswordHash, Role, RelatedID)
SELECT 
    CAST(StudentID AS NVARCHAR(50)) as Username,
    '123456' as PasswordHash,
    'Student' as Role,
    StudentID as RelatedID
FROM Students 
WHERE ClassID = @ClassID;

-- 添加管理员账号（如果不存在）
IF NOT EXISTS (SELECT 1 FROM Users WHERE Username = 'admin')
BEGIN
    INSERT INTO Users (Username, PasswordHash, Role, RelatedID) VALUES ('admin', 'admin123', 'Admin', 1);
END

IF NOT EXISTS (SELECT 1 FROM Users WHERE Username = 'teacher1')
BEGIN
    INSERT INTO Users (Username, PasswordHash, Role, RelatedID) VALUES ('teacher1', '123456', 'Teacher', 1);
END

PRINT '用户账号创建成功';

-- 6. 计算排名
EXEC sp_CalculateRankings '2024-2025', 1;
PRINT '排名计算完成';

-- 7. 插入一些示例加分项目
DECLARE @EvaluationID INT;

-- 为刘启源（最高分）添加加分项目
SELECT @EvaluationID = EvaluationID FROM ComprehensiveEvaluations WHERE StudentID = 3124001495;
INSERT INTO BonusDetails (EvaluationID, Category, ItemName, Score, Description) VALUES 
(@EvaluationID, 'C1', '创新创业团队立项', 10, '所加入的创新创业团队成功在学院立项'),
(@EvaluationID, 'C2', '互联网+大赛省赛金奖', 18, '中国国际"互联网+"大学生创新创业大赛省赛金奖担任一般成员'),
(@EvaluationID, 'S1', '班级学习委员', 32, '担任班级学习委员表现优秀'),
(@EvaluationID, 'W', '思政实践教学', 2, '广东工业大学思想政治理论课实践教学成果展示大赛二等奖');

-- 为吴彬源添加加分项目
SELECT @EvaluationID = EvaluationID FROM ComprehensiveEvaluations WHERE StudentID = 3124001502;
INSERT INTO BonusDetails (EvaluationID, Category, ItemName, Score, Description) VALUES 
(@EvaluationID, 'C1', '创新创业团队立项', 10, '所加入的创新创业团队成功在学校立项'),
(@EvaluationID, 'C2', '机器人大赛三等奖', 8, 'RoboCom机器人开发者大赛CAIP赛道省赛三等奖'),
(@EvaluationID, 'S1', '招生宣传协会干事', 30, '招生宣传协会优秀干事');

PRINT '示例加分项目添加完成';

-- 8. 显示导入结果
PRINT '=== 导入完成统计 ===';
SELECT '学生数量' as 项目, COUNT(*) as 数量 FROM Students WHERE ClassID = @ClassID
UNION ALL
SELECT '综测记录数量', COUNT(*) FROM ComprehensiveEvaluations
UNION ALL
SELECT '加分项目数量', COUNT(*) FROM BonusDetails
UNION ALL
SELECT '用户账号数量', COUNT(*) FROM Users;

PRINT '=== 综测排名前10名 ===';
SELECT TOP 10
    ClassRank as 排名,
    StudentName as 姓名,
    TotalScore as 总积分,
    GPA as 绩点,
    AcademicScore as 学业成绩
FROM v_ComprehensiveEvaluationDetails
WHERE AcademicYear = '2024-2025' AND Semester = 1
ORDER BY ClassRank;

PRINT '=== 数据导入完成！ ===';
GO
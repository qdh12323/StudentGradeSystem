-- 导入2024级数据科学与大数据技术2班综测数据
USE GradeSystemDB;
GO

PRINT '=== 开始导入综合测评数据 ===';

-- 1. 创建班级
DECLARE @ClassID INT;
INSERT INTO Classes (ClassName, Major, Grade, Advisor) 
VALUES ('数据科学与大数据技术2班', '数据科学与大数据技术', 2024, '待定');
SELECT @ClassID = SCOPE_IDENTITY();

-- 2. 导入学生基础信息
INSERT INTO Students (StudentID, Name, ClassID) VALUES 
(3124001479, '敖锦航', @ClassID),
(3124001480, '陈派煊', @ClassID),
(3124001481, '陈瑞健', @ClassID),
(3124001482, '陈书楷', @ClassID),
(3124001483, '陈文栩', @ClassID),
(3124001484, '陈修行', @ClassID),
(3124001485, '邓浩强', @ClassID),
(3124001486, '邓皓元', @ClassID),
(3124001487, '邓梓元', @ClassID),
(3124001489, '龚智康', @ClassID),
(3124001490, '胡鸿荣', @ClassID),
(3124001491, '黄文涛', @ClassID),
(3124001492, '梁百勋', @ClassID),
(3124001493, '刘焯林', @ClassID),
(3124001494, '刘俊良', @ClassID),
(3124001495, '刘启源', @ClassID),
(3124001496, '刘彦声', @ClassID),
(3124001497, '卢可居', @ClassID),
(3124001498, '陆薪宇', @ClassID),
(3124001499, '骆睿', @ClassID),
(3124001500, '潘宁昕', @ClassID),
(3124001501, '阮智信', @ClassID),
(3124001502, '吴彬源', @ClassID),
(3124001503, '向南飞', @ClassID),
(3124001504, '赵翔', @ClassID),
(3124001505, '郑承旭', @ClassID);

-- 3. 导入综合测评数据 (2024-2025学年第1学期)
INSERT INTO ComprehensiveEvaluations (
    StudentID, AcademicYear, Semester, 
    PhysicalScore, MoralScore, GPA, AcademicScore,
    InnovationBasicScore, InnovationBonusScore, InnovationTotalScore,
    StudentWorkScore, SocialServiceScore, SocialRewardScore, SocialTotalScore,
    CulturalSportsScore, TotalScore
) VALUES 
(3124001479, '2024-2025', 1, 85.9, 90, 3.1214, 81.214, 10, 18, 28, 0, 0, 0, 0, 6, 64.8498),
(3124001480, '2024-2025', 1, 83.2, 89, 2.0932, 70.932, 0, 0, 0, 20, 39, 0, 59, 0, 60.0024),
(3124001481, '2024-2025', 1, 52.3, 89.1, 3.5831, 85.831, 0, 0, 0, 0, 0, 0, 0, 0, 64.5367),
(3124001482, '2024-2025', 1, 79, 90, 2.9439, 79.439, 0, 0, 0, 20, 0, 0, 20, 0, 62.1073),
(3124001483, '2024-2025', 1, 80.8, 90, 3.8236, 88.236, 0, 0, 0, 33, 0, 0, 33, 2, 69.6652),
(3124001484, '2024-2025', 1, 85.8, 89.82, 3.5563, 85.563, 0, 0, 0, 0, 0, 0, 0, 2, 64.4851),
(3124001485, '2024-2025', 1, 76.3, 86.4, 2.7, 77, 0, 0, 0, 0, 0, 0, 0, 0, 58.22),
(3124001486, '2024-2025', 1, 79.8, 90, 2.9485, 79.485, 8, 0, 8, 30, 23, 0, 53, 0, 66.2395),
(3124001487, '2024-2025', 1, 60, 88.2, 2.1163, 71.163, 0, 0, 0, 8, 0, 0, 8, 2, 55.1241),
(3124001489, '2024-2025', 1, 72.6, 90, 2.1627, 71.627, 0, 0, 0, 20, 24, 10, 54, 0, 60.0389),
(3124001490, '2024-2025', 1, 77.3, 90, 3.2467, 82.467, 0, 0, 0, 0, 0, 0, 0, 0, 62.2269),
(3124001491, '2024-2025', 1, 65.4, 86, 1.6626, 66.626, 0, 0, 0, 8, 0, 0, 8, 0, 51.7382),
(3124001492, '2024-2025', 1, 60, 86.4, 2.3046, 73.046, 0, 0, 0, 0, 0, 0, 0, 0, 55.4522),
(3124001493, '2024-2025', 1, 74, 90, 3.3, 83, 10, 0, 10, 10, 0, 0, 10, 0, 64.6),
(3124001494, '2024-2025', 1, 59.4, 84.6, 1.4519, 64.519, 0, 0, 0, 0, 0, 0, 0, 0, 49.3933),
(3124001495, '2024-2025', 1, 72, 90, 3.785, 87.85, 20, 28, 48, 32, 39.5, 0, 71.5, 4, 78.145),
(3124001496, '2024-2025', 1, 78.7, 90, 1.9644, 69.644, 0, 0, 0, 8, 13, 0, 21, 2, 55.4508),
(3124001497, '2024-2025', 1, 78.2, 90, 3.1233, 81.233, 0, 3, 3, 30, 0, 0, 30, 0, 64.6631),
(3124001498, '2024-2025', 1, 65.4, 89.496, 3.4745, 84.745, 0, 0, 0, 22, 0, 0, 22, 2, 66.0963),
(3124001499, '2024-2025', 1, 64.4, 90, 2.7429, 77.429, 20, 0, 20, 20, 0, 10, 30, 0, 63.7003),
(3124001500, '2024-2025', 1, 80, 86.4, 2.6163, 76.163, 0, 0, 0, 0, 0, 0, 0, 2, 57.7341),
(3124001501, '2024-2025', 1, 57.8, 90, 3.1, 81, 20, 0.5, 20.5, 30, 40, 0, 70, 2, 70.35),
(3124001502, '2024-2025', 1, 81.6, 90, 3.5962, 85.962, 20, 8, 28, 30, 40, 0, 70, 2, 74.5734),
(3124001503, '2024-2025', 1, 61.3, 88.56, 3.2214, 82.214, 0, 0, 0, 0, 0, 0, 0, 0, 61.9778),
(3124001504, '2024-2025', 1, 90.4, 90, 3.6872, 86.872, 0, 0, 8, 20, 0, 0, 40, 2, 70.2104),
(3124001505, '2024-2025', 1, 81, 90, 2.158, 71.58, 0, 0, 0, 0, 0, 0, 0, 0, 58.158);

-- 4. 导入加分项目详情 (示例数据)
DECLARE @EvaluationID INT;

-- 敖锦航的加分项目
SELECT @EvaluationID = EvaluationID FROM ComprehensiveEvaluations WHERE StudentID = 3124001479;
INSERT INTO BonusDetails (EvaluationID, Category, ItemName, Score, Description) VALUES 
(@EvaluationID, 'C1', '创新创业团队立项', 10, '所加入的创新创业团队成功在学院立项'),
(@EvaluationID, 'C2', '互联网+大赛省赛金奖', 18, '中国国际"互联网+"大学生创新创业大赛省赛金奖担任一般成员'),
(@EvaluationID, 'W', '思政实践教学成果展示', 2, '广东工业大学2024-2025学年思想政治理论课实践教学成果展示大赛二等奖担任主要成员'),
(@EvaluationID, 'W', '同伴教育课', 2, '参与学校组织的同伴教育课');

-- 刘启源的加分项目 (综测最高分)
SELECT @EvaluationID = EvaluationID FROM ComprehensiveEvaluations WHERE StudentID = 3124001495;
INSERT INTO BonusDetails (EvaluationID, Category, ItemName, Score, Description) VALUES 
(@EvaluationID, 'C1', '创新创业团队立项', 10, '所加入的创新创业团队成功在学院立项'),
(@EvaluationID, 'C1', '学术科技类比赛', 12, '有效参与学院学术科技类高门槛比赛一次'),
(@EvaluationID, 'C2', '互联网+大赛省赛金奖', 18, '中国国际"互联网+"大学生创新创业大赛省赛金奖担任一般成员'),
(@EvaluationID, 'C2', '外语能力大赛银奖', 5, '2024"外研社国才杯""理解当代中国"全国大学生外语能力大赛校赛银奖'),
(@EvaluationID, 'C2', '英语词汇大赛三等奖', 5, '第五届"外教社词达人杯"全国大学生英语词汇能力大赛广东赛区本科非英语类专业组三等奖'),
(@EvaluationID, 'S1', '班级学习委员', 32, '担任班级学习委员表现优秀'),
(@EvaluationID, 'S2', '实践志愿活动', 39.5, '实践志愿活动'),
(@EvaluationID, 'W', '思政实践教学', 2, '广东工业大学2024-2025学年思想政治理论课实践教学成果展示大赛二等奖担任主要成员'),
(@EvaluationID, 'W', '同伴教育课', 2, '参与学校组织的同伴教育课');

-- 5. 计算排名
EXEC sp_CalculateRankings '2024-2025', 1;

-- 6. 创建用户账号
INSERT INTO Users (Username, PasswordHash, Role, RelatedID)
SELECT 
    CAST(StudentID AS NVARCHAR(50)) as Username,
    '123456' as PasswordHash,
    'Student' as Role,
    StudentID as RelatedID
FROM Students 
WHERE ClassID = @ClassID;

-- 添加管理员账号
INSERT INTO Users (Username, PasswordHash, Role, RelatedID) VALUES 
('admin', 'admin123', 'Admin', 1),
('teacher1', '123456', 'Teacher', 1);

-- 7. 显示导入结果
PRINT '=== 导入完成统计 ===';
SELECT '学生数量' as 项目, COUNT(*) as 数量 FROM Students WHERE ClassID = @ClassID
UNION ALL
SELECT '综测记录数量', COUNT(*) FROM ComprehensiveEvaluations
UNION ALL
SELECT '加分项目数量', COUNT(*) FROM BonusDetails;

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

PRINT '数据导入完成！';
GO
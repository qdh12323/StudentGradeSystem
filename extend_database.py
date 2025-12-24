#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库扩展脚本
执行数据库结构扩展和示例数据插入
"""

import pyodbc
from datetime import datetime

# 数据库连接配置
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;" 
    "DATABASE=GradeSystemDB;"
    "Trusted_Connection=yes;"
)

def execute_sql_script():
    """执行数据库扩展脚本"""
    print("=== 开始扩展数据库结构 ===")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # 1. 扩展Students表
        print("1. 扩展Students表...")
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM sys.columns 
                WHERE object_id = OBJECT_ID('Students') AND name = 'Gender'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE Students ADD 
                        Gender NVARCHAR(10),
                        Birthdate DATE,
                        Hometown NVARCHAR(100),
                        IDCard NVARCHAR(18),
                        Phone NVARCHAR(20),
                        Email NVARCHAR(100),
                        Address NVARCHAR(200),
                        EnrollmentDate DATE,
                        Status NVARCHAR(20) DEFAULT '在读',
                        CreatedAt DATETIME DEFAULT GETDATE(),
                        UpdatedAt DATETIME DEFAULT GETDATE()
                """)
                print("   ✅ Students表扩展完成")
            else:
                print("   ✅ Students表已扩展，跳过")
        except Exception as e:
            print(f"   ⚠️ Students表扩展警告: {e}")
        
        # 2. 创建Courses表
        print("2. 创建Courses表...")
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM sys.tables WHERE name = 'Courses'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    CREATE TABLE Courses (
                        CourseID INT PRIMARY KEY IDENTITY(1,1),
                        CourseCode NVARCHAR(20) UNIQUE NOT NULL,
                        CourseName NVARCHAR(100) NOT NULL,
                        Credits DECIMAL(3,1) NOT NULL,
                        Hours INT NOT NULL,
                        CourseType NVARCHAR(20) DEFAULT '必修',
                        Department NVARCHAR(50),
                        Prerequisites NVARCHAR(200),
                        Description NTEXT,
                        Status NVARCHAR(20) DEFAULT '开设',
                        CreatedAt DATETIME DEFAULT GETDATE(),
                        UpdatedAt DATETIME DEFAULT GETDATE()
                    )
                """)
                print("   ✅ Courses表创建完成")
            else:
                print("   ✅ Courses表已存在，跳过")
        except Exception as e:
            print(f"   ❌ Courses表创建失败: {e}")
        
        # 3. 创建CourseOfferings表
        print("3. 创建CourseOfferings表...")
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM sys.tables WHERE name = 'CourseOfferings'
            """)
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    CREATE TABLE CourseOfferings (
                        OfferingID INT PRIMARY KEY IDENTITY(1,1),
                        CourseID INT NOT NULL,
                        TeacherName NVARCHAR(50),
                        AcademicYear NVARCHAR(20),
                        Semester INT,
                        ClassTime NVARCHAR(100),
                        Classroom NVARCHAR(50),
                        MaxStudents INT DEFAULT 50,
                        CurrentStudents INT DEFAULT 0,
                        CreatedAt DATETIME DEFAULT GETDATE(),
                        FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
                    )
                """)
                print("   ✅ CourseOfferings表创建完成")
            else:
                print("   ✅ CourseOfferings表已存在，跳过")
        except Exception as e:
            print(f"   ❌ CourseOfferings表创建失败: {e}")
        
        # 4. 插入示例课程数据
        print("4. 插入示例课程数据...")
        try:
            cursor.execute("SELECT COUNT(*) FROM Courses")
            if cursor.fetchone()[0] == 0:
                courses_data = [
                    ('CS001', '数据结构与算法', 4.0, 64, '必修', '计算机学院', '学习基本的数据结构和算法设计'),
                    ('CS002', '数据库原理与应用', 3.5, 56, '必修', '计算机学院', '关系数据库理论与SQL应用'),
                    ('CS003', 'Java程序设计', 3.0, 48, '必修', '计算机学院', 'Java面向对象编程'),
                    ('CS004', 'Web前端开发', 2.5, 40, '选修', '计算机学院', 'HTML、CSS、JavaScript开发'),
                    ('CS005', '机器学习基础', 3.0, 48, '选修', '计算机学院', '机器学习算法与应用'),
                    ('MATH001', '高等数学A', 5.0, 80, '必修', '数学学院', '微积分基础理论'),
                    ('MATH002', '线性代数', 3.0, 48, '必修', '数学学院', '矩阵理论与线性方程组'),
                    ('ENG001', '大学英语', 2.0, 32, '必修', '外语学院', '英语听说读写综合训练')
                ]
                
                for course in courses_data:
                    cursor.execute("""
                        INSERT INTO Courses (CourseCode, CourseName, Credits, Hours, CourseType, Department, Description)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, course)
                print(f"   ✅ 插入了{len(courses_data)}门课程")
            else:
                print("   ✅ 课程数据已存在，跳过")
        except Exception as e:
            print(f"   ❌ 插入课程数据失败: {e}")
        
        # 5. 插入课程开设信息
        print("5. 插入课程开设信息...")
        try:
            cursor.execute("SELECT COUNT(*) FROM CourseOfferings")
            if cursor.fetchone()[0] == 0:
                offerings_data = [
                    (1, '张教授', '2024-2025', 1, '周一3-4节，周三5-6节', 'A101'),
                    (2, '李教授', '2024-2025', 1, '周二1-2节，周四3-4节', 'B201'),
                    (3, '王老师', '2024-2025', 1, '周一5-6节，周五1-2节', 'C301'),
                    (4, '赵老师', '2024-2025', 2, '周三1-2节，周五3-4节', 'D401'),
                    (5, '陈教授', '2024-2025', 2, '周二5-6节，周四1-2节', 'E501')
                ]
                
                for offering in offerings_data:
                    cursor.execute("""
                        INSERT INTO CourseOfferings (CourseID, TeacherName, AcademicYear, Semester, ClassTime, Classroom)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, offering)
                print(f"   ✅ 插入了{len(offerings_data)}个课程开设记录")
            else:
                print("   ✅ 课程开设数据已存在，跳过")
        except Exception as e:
            print(f"   ❌ 插入课程开设数据失败: {e}")
        
        # 6. 更新现有学生信息
        print("6. 更新现有学生信息...")
        try:
            cursor.execute("""
                UPDATE Students SET 
                    Gender = CASE 
                        WHEN Name IN ('刘启源', '吴彬源', '邓浩强', '邓皓元', '龚智康', '胡鸿荣', '黄文涛', '梁百勋', '刘焯林', '刘俊良', '刘彦声', '卢可居', '陆薪宇', '骆睿', '潘宁昕', '阮智信', '向南飞', '赵翔', '郑承旭') THEN '男'
                        ELSE '女'
                    END,
                    Hometown = '广东省',
                    EnrollmentDate = '2024-09-01',
                    Status = '在读',
                    UpdatedAt = GETDATE()
                WHERE Gender IS NULL
            """)
            updated_count = cursor.rowcount
            print(f"   ✅ 更新了{updated_count}名学生的基本信息")
        except Exception as e:
            print(f"   ❌ 更新学生信息失败: {e}")
        
        # 提交所有更改
        conn.commit()
        
        # 7. 验证扩展结果
        print("\n7. 验证扩展结果...")
        
        # 检查表结构
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"   数据库表: {', '.join(tables)}")
        
        # 检查数据量
        cursor.execute("SELECT COUNT(*) FROM Students")
        student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Courses")
        course_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM CourseOfferings")
        offering_count = cursor.fetchone()[0]
        
        print(f"   学生数量: {student_count}")
        print(f"   课程数量: {course_count}")
        print(f"   开设课程数量: {offering_count}")
        
        print("\n🎉 数据库扩展完成！")
        return True
        
    except Exception as e:
        print(f"❌ 数据库扩展失败: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    success = execute_sql_script()
    if success:
        print("\n✅ 可以继续进行后端API开发")
    else:
        print("\n❌ 请检查数据库连接和权限")
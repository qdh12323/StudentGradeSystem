#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库验证脚本
用于检查数据库表结构和数据是否正确导入
"""

import pyodbc
import pandas as pd
from datetime import datetime

# 数据库连接配置
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;" 
    "DATABASE=GradeSystemDB;"
    "Trusted_Connection=yes;"
)

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("请检查:")
        print("1. SQL Server 是否启动")
        print("2. 数据库 GradeSystemDB 是否存在")
        print("3. 连接字符串是否正确")
        return None

def verify_database():
    """验证数据库结构和数据"""
    print("=== 数据库验证开始 ===")
    print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # 1. 检查数据库是否存在
        print("1. 检查数据库...")
        cursor.execute("SELECT DB_NAME() as CurrentDatabase")
        db_name = cursor.fetchone()[0]
        if db_name == 'GradeSystemDB':
            print("✅ 数据库 GradeSystemDB 连接成功")
        else:
            print(f"❌ 当前连接的数据库是: {db_name}")
            return False
        
        print()
        
        # 2. 检查表结构
        print("2. 检查表结构...")
        expected_tables = [
            'Students', 'ComprehensiveEvaluations', 'BonusDetails', 
            'Classes', 'Users'
        ]
        
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"   现有表: {', '.join(existing_tables)}")
        
        missing_tables = [table for table in expected_tables if table not in existing_tables]
        if missing_tables:
            print(f"❌ 缺少表: {', '.join(missing_tables)}")
            print("   请执行 comprehensive_evaluation_schema.sql 创建表结构")
            return False
        else:
            print("✅ 所有必需的表都存在")
        
        print()
        
        # 3. 检查数据量
        print("3. 检查数据量...")
        tables_data = {}
        
        for table in expected_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            tables_data[table] = count
            print(f"   {table}: {count} 条记录")
        
        print()
        
        # 4. 检查关键数据
        print("4. 检查关键数据...")
        
        # 检查班级数据
        cursor.execute("SELECT ClassID, ClassName, Major FROM Classes")
        classes = cursor.fetchall()
        if classes:
            print("✅ 班级数据:")
            for cls in classes:
                print(f"   - {cls[1]} ({cls[2]}) [ID: {cls[0]}]")
        else:
            print("❌ 没有班级数据")
        
        print()
        
        # 检查学生数据
        cursor.execute("""
            SELECT TOP 5 StudentID, Name, ClassName 
            FROM Students s
            JOIN Classes c ON s.ClassID = c.ClassID
            ORDER BY StudentID
        """)
        students = cursor.fetchall()
        if students:
            print("✅ 学生数据 (前5名):")
            for student in students:
                print(f"   - {student[0]}: {student[1]} ({student[2]})")
        else:
            print("❌ 没有学生数据")
        
        print()
        
        # 检查综测数据
        cursor.execute("""
            SELECT COUNT(*) as 综测记录数,
                   AVG(TotalScore) as 平均总积分,
                   MAX(TotalScore) as 最高总积分,
                   MIN(TotalScore) as 最低总积分
            FROM ComprehensiveEvaluations
            WHERE TotalScore IS NOT NULL
        """)
        eval_stats = cursor.fetchone()
        if eval_stats and eval_stats[0] > 0:
            print("✅ 综测数据统计:")
            print(f"   - 记录数: {eval_stats[0]}")
            print(f"   - 平均总积分: {eval_stats[1]:.2f}")
            print(f"   - 最高总积分: {eval_stats[2]:.2f}")
            print(f"   - 最低总积分: {eval_stats[3]:.2f}")
        else:
            print("❌ 没有综测数据")
        
        print()
        
        # 检查用户账号
        cursor.execute("""
            SELECT Role, COUNT(*) as 数量
            FROM Users
            GROUP BY Role
            ORDER BY Role
        """)
        user_stats = cursor.fetchall()
        if user_stats:
            print("✅ 用户账号统计:")
            for stat in user_stats:
                print(f"   - {stat[0]}: {stat[1]} 个账号")
        else:
            print("❌ 没有用户账号")
        
        print()
        
        # 5. 检查视图和存储过程
        print("5. 检查视图和存储过程...")
        
        # 检查视图
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.VIEWS
            WHERE TABLE_NAME = 'v_ComprehensiveEvaluationDetails'
        """)
        view_exists = cursor.fetchone()
        if view_exists:
            print("✅ 视图 v_ComprehensiveEvaluationDetails 存在")
        else:
            print("❌ 视图 v_ComprehensiveEvaluationDetails 不存在")
        
        # 检查存储过程
        cursor.execute("""
            SELECT ROUTINE_NAME 
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_TYPE = 'PROCEDURE' 
            AND ROUTINE_NAME IN ('sp_CalculateComprehensiveScore', 'sp_CalculateRankings')
        """)
        procedures = [row[0] for row in cursor.fetchall()]
        expected_procedures = ['sp_CalculateComprehensiveScore', 'sp_CalculateRankings']
        
        for proc in expected_procedures:
            if proc in procedures:
                print(f"✅ 存储过程 {proc} 存在")
            else:
                print(f"❌ 存储过程 {proc} 不存在")
        
        print()
        
        # 6. 测试视图查询
        print("6. 测试视图查询...")
        try:
            cursor.execute("""
                SELECT TOP 3 StudentName, TotalScore, ClassRank
                FROM v_ComprehensiveEvaluationDetails
                WHERE AcademicYear = '2024-2025' AND Semester = 1
                ORDER BY ClassRank
            """)
            top_students = cursor.fetchall()
            if top_students:
                print("✅ 视图查询成功，前3名学生:")
                for i, student in enumerate(top_students, 1):
                    print(f"   {i}. {student[0]} - {student[1]:.2f}分 (排名: {student[2]})")
            else:
                print("⚠️  视图查询成功但没有数据")
        except Exception as e:
            print(f"❌ 视图查询失败: {e}")
        
        print()
        
        # 7. 验证总结
        print("=== 验证总结 ===")
        
        issues = []
        if tables_data['Students'] == 0:
            issues.append("缺少学生数据")
        if tables_data['ComprehensiveEvaluations'] == 0:
            issues.append("缺少综测数据")
        if tables_data['Users'] == 0:
            issues.append("缺少用户账号")
        if tables_data['Classes'] == 0:
            issues.append("缺少班级数据")
        
        if not issues:
            print("🎉 数据库验证通过！所有数据都已正确导入。")
            print("\n可以正常启动系统:")
            print("1. 启动后端: python backend/main.py")
            print("2. 启动前端: cd frontend && npm run dev")
            print("3. 访问: http://localhost:5173")
            return True
        else:
            print("❌ 发现以下问题:")
            for issue in issues:
                print(f"   - {issue}")
            print("\n建议操作:")
            print("1. 执行 database/comprehensive_evaluation_schema.sql 创建表结构")
            print("2. 执行 database/import_comprehensive_data.sql 导入数据")
            return False
            
    except Exception as e:
        print(f"❌ 验证过程中出错: {e}")
        return False
    finally:
        conn.close()

def show_sample_data():
    """显示示例数据"""
    print("\n=== 示例数据预览 ===")
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # 显示综测排名
        query = """
            SELECT TOP 10
                ClassRank as 排名,
                StudentName as 姓名,
                TotalScore as 总积分,
                GPA as 绩点,
                AcademicScore as 学业成绩,
                InnovationTotalScore as 创新实践,
                SocialTotalScore as 社会实践
            FROM v_ComprehensiveEvaluationDetails
            WHERE AcademicYear = '2024-2025' AND Semester = 1
            ORDER BY ClassRank
        """
        
        df = pd.read_sql(query, conn)
        if not df.empty:
            print("综测排名前10名:")
            print(df.to_string(index=False, float_format='%.2f'))
        else:
            print("没有综测数据可显示")
            
    except Exception as e:
        print(f"查询示例数据失败: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    success = verify_database()
    if success:
        show_sample_data()
    
    print(f"\n验证完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
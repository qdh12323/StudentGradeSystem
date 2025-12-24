#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
自动执行SQL脚本来创建表结构和导入数据
"""

import pyodbc
import os
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
        print("3. 如果数据库不存在，请先创建: CREATE DATABASE GradeSystemDB;")
        return None

def execute_sql_file(conn, file_path, description):
    """执行SQL文件"""
    print(f"正在执行: {description}")
    print(f"文件: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # 分割SQL语句（以GO为分隔符）
        sql_commands = sql_content.split('GO')
        
        cursor = conn.cursor()
        
        for i, command in enumerate(sql_commands):
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    conn.commit()
                except Exception as e:
                    print(f"⚠️  执行第{i+1}个命令时出错: {e}")
                    print(f"命令内容: {command[:100]}...")
                    # 继续执行其他命令
        
        cursor.close()
        print(f"✅ {description} 执行完成")
        return True
        
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

def init_database():
    """初始化数据库"""
    print("=== 数据库初始化开始 ===")
    print(f"初始化时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        # 1. 创建表结构
        schema_file = "database/comprehensive_evaluation_schema.sql"
        if not execute_sql_file(conn, schema_file, "创建综合测评表结构"):
            print("❌ 表结构创建失败")
            return False
        
        print()
        
        # 2. 导入数据
        data_file = "database/import_comprehensive_data.sql"
        if not execute_sql_file(conn, data_file, "导入综合测评数据"):
            print("❌ 数据导入失败")
            return False
        
        print()
        print("🎉 数据库初始化完成！")
        return True
        
    except Exception as e:
        print(f"❌ 初始化过程中出错: {e}")
        return False
    finally:
        conn.close()

def create_database_if_not_exists():
    """如果数据库不存在则创建"""
    print("检查数据库是否存在...")
    
    # 连接到master数据库
    master_conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;" 
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )
    
    try:
        conn = pyodbc.connect(master_conn_str)
        cursor = conn.cursor()
        
        # 检查数据库是否存在
        cursor.execute("SELECT name FROM sys.databases WHERE name = 'GradeSystemDB'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print("数据库不存在，正在创建...")
            cursor.execute("CREATE DATABASE GradeSystemDB")
            conn.commit()
            print("✅ 数据库 GradeSystemDB 创建成功")
        else:
            print("✅ 数据库 GradeSystemDB 已存在")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查/创建失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 学生成绩管理系统 - 数据库初始化 ===")
    print()
    
    # 1. 检查并创建数据库
    if not create_database_if_not_exists():
        print("数据库创建失败，请手动创建数据库后重试")
        exit(1)
    
    print()
    
    # 2. 初始化表结构和数据
    if init_database():
        print()
        print("=== 初始化成功 ===")
        print("现在可以:")
        print("1. 运行验证脚本: python verify_database.py")
        print("2. 启动后端服务: python backend/main.py")
        print("3. 启动前端服务: cd frontend && npm run dev")
    else:
        print()
        print("=== 初始化失败 ===")
        print("请检查错误信息并手动执行SQL脚本")
    
    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统测试脚本
用于验证后端API是否正常工作
"""

import requests
import json

# 后端API基础URL
BASE_URL = "http://127.0.0.1:8000"

def test_api():
    """测试API接口"""
    print("=== 学生成绩管理系统 API 测试 ===\n")
    
    # 1. 测试健康检查
    print("1. 测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            print(f"   响应: {response.json()}")
        else:
            print("❌ 健康检查失败")
            print(f"   状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("   请确保后端服务已启动 (python backend/main.py)")
        return False
    
    print()
    
    # 2. 测试用户列表
    print("2. 测试用户列表...")
    try:
        response = requests.get(f"{BASE_URL}/api/test/users")
        if response.status_code == 200:
            users = response.json()
            print("✅ 用户列表获取成功")
            print(f"   用户数量: {len(users.get('users', []))}")
            for user in users.get('users', [])[:3]:  # 显示前3个用户
                print(f"   - {user['username']} ({user['role']})")
        else:
            print("❌ 用户列表获取失败")
            print(f"   状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    
    # 3. 测试登录
    print("3. 测试登录...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{BASE_URL}/api/login", json=login_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ 登录测试成功")
            print(f"   角色: {result.get('role')}")
        else:
            print("❌ 登录测试失败")
            print(f"   状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 登录请求失败: {e}")
    
    print()
    
    # 4. 测试综测排名列表
    print("4. 测试综测排名列表...")
    try:
        params = {
            "academic_year": "2024-2025",
            "semester": 1,
            "limit": 5
        }
        response = requests.get(f"{BASE_URL}/api/ranking/list", params=params)
        if response.status_code == 200:
            result = response.json()
            rankings = result.get('rankings', [])
            print("✅ 综测排名获取成功")
            print(f"   记录数量: {len(rankings)}")
            if rankings:
                print("   前3名:")
                for i, student in enumerate(rankings[:3]):
                    print(f"   {i+1}. {student.get('StudentName', 'N/A')} - {student.get('TotalScore', 0):.2f}分")
        else:
            print("❌ 综测排名获取失败")
            print(f"   状态码: {response.status_code}")
            if response.status_code == 500:
                print("   可能是数据库连接问题，请检查数据库配置")
    except Exception as e:
        print(f"❌ 请求失败: {e}")
    
    print()
    print("=== 测试完成 ===")
    print("\n如果所有测试都通过，说明后端API正常工作")
    print("现在可以启动前端进行完整测试:")
    print("cd frontend && npm run dev")
    
    return True

if __name__ == "__main__":
    test_api()
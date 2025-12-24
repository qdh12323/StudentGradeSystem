import React, { useState, useEffect } from 'react';
import { Card, Button, message, Space, Divider } from 'antd';
import api from '../utils/api';

const TestPage: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<string>('未测试');
  const [userCount, setUserCount] = useState<number>(0);
  const [loading, setLoading] = useState(false);

  // 测试API连接
  const testApiConnection = async () => {
    setLoading(true);
    try {
      const response = await api.get('/');
      setApiStatus('连接成功');
      message.success('后端API连接正常');
    } catch (error) {
      setApiStatus('连接失败');
      message.error('后端API连接失败，请检查后端服务是否启动');
      console.error('API连接错误:', error);
    } finally {
      setLoading(false);
    }
  };

  // 测试用户数据
  const testUserData = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/test/users');
      const users = response.data.users || [];
      setUserCount(users.length);
      message.success(`获取到 ${users.length} 个用户`);
    } catch (error) {
      message.error('获取用户数据失败');
      console.error('用户数据错误:', error);
    } finally {
      setLoading(false);
    }
  };

  // 测试登录
  const testLogin = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/login', {
        username: 'admin',
        password: 'admin123'
      });
      message.success(`登录成功，角色: ${response.data.role}`);
    } catch (error) {
      message.error('登录测试失败');
      console.error('登录错误:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card title="系统测试页面" style={{ maxWidth: 600 }}>
        <Space direction="vertical" style={{ width: '100%' }}>
          <div>
            <strong>API连接状态:</strong> {apiStatus}
          </div>
          <div>
            <strong>用户数量:</strong> {userCount}
          </div>
          
          <Divider />
          
          <Space>
            <Button 
              type="primary" 
              onClick={testApiConnection}
              loading={loading}
            >
              测试API连接
            </Button>
            <Button 
              onClick={testUserData}
              loading={loading}
            >
              测试用户数据
            </Button>
            <Button 
              onClick={testLogin}
              loading={loading}
            >
              测试登录
            </Button>
          </Space>

          <Divider />

          <div style={{ fontSize: '12px', color: '#666' }}>
            <p><strong>使用说明:</strong></p>
            <p>1. 确保后端服务已启动 (python backend/main.py)</p>
            <p>2. 确保数据库已配置并导入数据</p>
            <p>3. 点击上方按钮测试各项功能</p>
          </div>
        </Space>
      </Card>
    </div>
  );
};

export default TestPage;
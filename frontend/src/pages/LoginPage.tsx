import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import axios from 'axios';
import { UserState } from '../App';

// #region agent log
const logDebug = (location: string, message: string, data: any, hypothesisId: string) => {
  fetch('http://127.0.0.1:7244/ingest/d70bd03f-0689-4b0f-b937-3c68842f8ea0', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, message, data, timestamp: Date.now(), sessionId: 'debug-session', runId: 'run1', hypothesisId })
  }).catch(() => {});
};
// #endregion

interface LoginPageProps {
  onLogin: (user: UserState) => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  // #region agent log
  logDebug('LoginPage.tsx:20', 'LoginPage component function entry', {}, 'A');
  // #endregion
  
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleLogin = async (values: { username: string; password: string }) => {
    // #region agent log
    logDebug('LoginPage.tsx:28', 'Login attempt started', { username: values.username }, 'A');
    // #endregion
    
    setLoading(true);
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/login', {
        username: values.username,
        password: values.password
      });
      
      // #region agent log
      logDebug('LoginPage.tsx:37', 'Login API response received', { status: res.status, data: res.data }, 'A');
      // #endregion
      
      if (res.data.status === 'success') {
        const userState: UserState = {
          isLoggedIn: true,
          role: res.data.role,
          relatedId: res.data.related_id
        };
        onLogin(userState);
        // #region agent log
        logDebug('LoginPage.tsx:47', 'Login success, navigating to dashboard', { userState }, 'A');
        // #endregion
        navigate('/dashboard');
      }
    } catch (error: any) {
      // #region agent log
      logDebug('LoginPage.tsx:53', 'Login API error', { error: error?.message || String(error), response: error?.response?.data }, 'A');
      // #endregion
      message.error(error?.response?.data?.detail || '登录失败，请检查用户名和密码');
    } finally {
      setLoading(false);
    }
  };

  // #region agent log
  logDebug('LoginPage.tsx:60', 'LoginPage render starting', {}, 'A');
  // #endregion

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f0f2f5' }}>
      <Card title="学生成绩管理系统 - 登录" style={{ width: 400 }}>
        <Form
          name="login"
          onFinish={handleLogin}
          autoComplete="off"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名!' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="用户名" />
          </Form.Item>
          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码!' }]}
          >
            <Input.Password prefix={<LockOutlined />} placeholder="密码" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading} block>
              登录
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}

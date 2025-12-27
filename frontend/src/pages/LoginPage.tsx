import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, Card, message, Typography } from 'antd';
import { UserOutlined, LockOutlined, TeamOutlined } from '@ant-design/icons';
import axios from 'axios';
import { UserState } from '../App';

const { Title, Text } = Typography;

interface LoginPageProps {
  onLogin: (user: UserState) => void;
}

export default function LoginPage({ onLogin }: LoginPageProps) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleLogin = async (values: { username: string; password: string }) => {
    setLoading(true);
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/login', {
        username: values.username,
        password: values.password
      });
      
      if (res.data.status === 'success') {
        const userState: UserState = {
          isLoggedIn: true,
          role: res.data.role,
          relatedId: res.data.related_id
        };
        onLogin(userState);
        navigate('/dashboard');
      }
    } catch (error: any) {
      message.error(error?.response?.data?.detail || '登录失败，请检查用户名和密码');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      {/* 背景装饰 */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'url(/images/class-photo.png) center/contain no-repeat',
        opacity: 0.05,
        zIndex: 0
      }} />
      
      {/* 主要内容区域 */}
      <div style={{
        display: 'flex',
        maxWidth: '1200px',
        width: '100%',
        background: 'rgba(255, 255, 255, 0.95)',
        borderRadius: '20px',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
        overflow: 'hidden',
        zIndex: 1,
        position: 'relative'
      }}>
        {/* 左侧班级照片区域 */}
        <div style={{
          flex: 1,
          background: 'url(/images/class-photo.png) center/contain no-repeat',
          backgroundColor: '#f0f2f5',
          minHeight: '500px',
          position: 'relative',
          display: 'flex',
          alignItems: 'flex-end',
          padding: '40px'
        }}>
          <div style={{
            background: 'rgba(0, 0, 0, 0.7)',
            color: 'white',
            padding: '20px',
            borderRadius: '10px',
            backdropFilter: 'blur(10px)'
          }}>
            <Title level={3} style={{ color: 'white', margin: 0, marginBottom: '8px' }}>
              <TeamOutlined style={{ marginRight: '8px' }} />
              2024级数据科学与大数据技术2班
            </Title>
            <Text style={{ color: 'rgba(255, 255, 255, 0.9)' }}>
              团结 · 进步 · 创新 · 卓越
            </Text>
          </div>
        </div>

        {/* 右侧登录表单区域 */}
        <div style={{
          flex: 1,
          padding: '60px 40px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          background: 'white'
        }}>
          <div style={{ textAlign: 'center', marginBottom: '40px' }}>
            <Title level={2} style={{ 
              color: '#1890ff', 
              marginBottom: '8px',
              fontSize: '28px',
              fontWeight: 'bold'
            }}>
              大数据2班管理系统
            </Title>
            <Text style={{ 
              color: '#666', 
              fontSize: '16px'
            }}>
              欢迎登录班级综合管理平台
            </Text>
          </div>

          <Card 
            bordered={false}
            style={{ 
              boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
              borderRadius: '12px'
            }}
          >
            <Form
              name="login"
              onFinish={handleLogin}
              autoComplete="off"
              size="large"
            >
              <Form.Item
                name="username"
                rules={[{ required: true, message: '请输入用户名!' }]}
              >
                <Input 
                  prefix={<UserOutlined style={{ color: '#1890ff' }} />} 
                  placeholder="请输入用户名"
                  style={{ 
                    borderRadius: '8px',
                    height: '48px'
                  }}
                />
              </Form.Item>
              
              <Form.Item
                name="password"
                rules={[{ required: true, message: '请输入密码!' }]}
              >
                <Input.Password 
                  prefix={<LockOutlined style={{ color: '#1890ff' }} />} 
                  placeholder="请输入密码"
                  style={{ 
                    borderRadius: '8px',
                    height: '48px'
                  }}
                />
              </Form.Item>
              
              <Form.Item style={{ marginBottom: '16px' }}>
                <Button 
                  type="primary" 
                  htmlType="submit" 
                  loading={loading} 
                  block
                  style={{
                    height: '48px',
                    borderRadius: '8px',
                    fontSize: '16px',
                    fontWeight: 'bold',
                    background: 'linear-gradient(135deg, #1890ff, #096dd9)',
                    border: 'none'
                  }}
                >
                  立即登录
                </Button>
              </Form.Item>
            </Form>
            
            <div style={{ 
              textAlign: 'center', 
              marginTop: '20px',
              padding: '16px',
              background: '#f8f9fa',
              borderRadius: '8px'
            }}>
              <Text style={{ color: '#666', fontSize: '14px' }}>
                💡 登录提示：管理员 admin/admin123 | 教师 teacher1/123456 | 学生 学号/123456
              </Text>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
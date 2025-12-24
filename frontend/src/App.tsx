import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import { ConfigProvider } from 'antd';

// 定义用户状态类型
export interface UserState {
  isLoggedIn: boolean;
  role: 'Teacher' | 'Student' | 'Admin' | null;
  relatedId: number | null;
}

function App() {
  // 这里的状态管理较简单，实际项目可用 Redux 或 Context
  const [user, setUser] = useState<UserState>({
    isLoggedIn: false,
    role: null,
    relatedId: null
  });

  return (
    <ConfigProvider theme={{ token: { colorPrimary: '#1677ff' } }}>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage onLogin={setUser} />} />
          <Route 
            path="/dashboard" 
            element={user.isLoggedIn ? <Dashboard user={user} /> : <Navigate to="/login" />} 
          />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
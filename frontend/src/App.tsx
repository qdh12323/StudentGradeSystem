import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import { ConfigProvider } from 'antd';

// #region agent log
const logDebug = (location: string, message: string, data: any, hypothesisId: string) => {
  fetch('http://127.0.0.1:7244/ingest/d70bd03f-0689-4b0f-b937-3c68842f8ea0', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location, message, data, timestamp: Date.now(), sessionId: 'debug-session', runId: 'run1', hypothesisId })
  }).catch(() => {});
};
// #endregion

// 定义用户状态类型
export interface UserState {
  isLoggedIn: boolean;
  role: 'Teacher' | 'Student' | null;
  relatedId: number | null;
}

function App() {
  // #region agent log
  logDebug('App.tsx:24', 'App component function entry', {}, 'B');
  // #endregion
  
  // 这里的状态管理较简单，实际项目可用 Redux 或 Context
  const [user, setUser] = useState<UserState>({
    isLoggedIn: false,
    role: null,
    relatedId: null
  });

  // #region agent log
  logDebug('App.tsx:32', 'App state initialized', { userState: user }, 'B');
  // #endregion

  // #region agent log
  logDebug('App.tsx:35', 'App render starting, about to render routes', { currentPath: window.location.pathname }, 'B');
  // #endregion

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
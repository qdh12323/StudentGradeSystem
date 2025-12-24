import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:8001',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等认证信息
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 统一错误处理
    if (error.response?.status === 401) {
      // 未授权，跳转到登录页
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
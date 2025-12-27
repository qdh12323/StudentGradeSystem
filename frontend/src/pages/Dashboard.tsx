import React, { useState, useEffect } from 'react';
import { Layout, Menu, Table, Button, Modal, Form, InputNumber, message, Card, Row, Col, Tag } from 'antd';
import { 
  UserOutlined, BookOutlined, LogoutOutlined, DollarOutlined, 
  FileExcelOutlined, PlusOutlined, TrophyOutlined, BarChartOutlined, BugOutlined,
  TeamOutlined, ReadOutlined
} from '@ant-design/icons';
import axios from 'axios';
import ComprehensiveEvaluation from './ComprehensiveEvaluation';
import StudentManagement from './StudentManagement';
import CourseManagement from './CourseManagement';
import TestPage from './TestPage';

import { UserState } from '../App';

const { Header, Content, Sider } = Layout;
interface DashboardProps {
  user: UserState;
}

export default function Dashboard({ user }: DashboardProps) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]); // 表格数据
  const [currentPage, setCurrentPage] = useState('grades'); // 当前页面

  // 定义表格列
  const columns = [
    { title: '学号', dataIndex: 'StudentID', key: 'StudentID' },
    { title: '姓名', dataIndex: 'Name', key: 'Name' },
    { title: '课程', dataIndex: 'CourseName', key: 'CourseName' },
    { title: '平时(10%)', dataIndex: 'RegularScore', key: 'RegularScore' },
    { title: '期中(30%)', dataIndex: 'MidtermScore', key: 'MidtermScore' },
    { title: '期末(60%)', dataIndex: 'FinalScore', key: 'FinalScore' },
    { 
      title: '总评', 
      dataIndex: 'TotalScore', 
      key: 'TotalScore',
      render: (score: number) => <Tag color={score < 60 ? 'red' : 'green'}>{score}</Tag> 
    },
  ];

  // 加载数据 (这里先简单模拟，实际应调用后端查询接口)
  const fetchData = async () => {
    // 你可以在 main.py 加一个 @app.get("/api/grades/list") 来获取真实数据
    // 这里为了演示先留空，或者你可以自行扩展
    // const res = await axios.get('http://127.0.0.1:8000/api/grades/list');
    // setData(res.data);
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 录入成绩
  const handleAddGrade = async (values: any) => {
    try {
      await axios.post('http://127.0.0.1:8000/api/grades/add', {
        student_id: values.student_id,
        course_id: values.course_id,
        regular_score: values.regular,
        midterm_score: values.midterm,
        final_score: values.final
      });
      message.success('成绩录入成功！');
      setIsModalOpen(false);
      fetchData(); // 刷新表格
    } catch (error) {
      message.error('录入失败，请检查学号或课程ID是否存在');
    }
  };

  // 结算奖学金
  const handleSettle = async () => {
    setLoading(true);
    try {
      await axios.post('http://127.0.0.1:8000/api/scholarship/settle', {
        year: 2025,
        term: 1
      });
      message.success('奖学金计算完成！请查看数据库 Scholarships 表');
    } catch (error) {
      message.error('计算失败');
    }
    setLoading(false);
  };

  // 导出 Excel
  const handleExport = () => {
    // 浏览器直接下载
    window.open(`http://127.0.0.1:8000/api/export/grades?class_id=${user.role === 'Teacher' ? '' : 'my'}`, '_blank');
  };

  // 渲染页面内容
  const renderContent = () => {
    switch (currentPage) {
      case 'comprehensive':
        return <ComprehensiveEvaluation user={user} />;
      case 'students':
        return <StudentManagement user={user} />;
      case 'courses':
        return <CourseManagement user={user} />;
      case 'test':
        return <TestPage />;
      case 'grades':
      default:
        return (
          <>
            {/* 只有老师可见的操作区 */}
            {user.role === 'Teacher' && (
              <Card style={{ marginBottom: 20, background: '#fafafa' }} bordered={false}>
                <Row gutter={16}>
                  <Col>
                    <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>
                      录入/修改成绩
                    </Button>
                  </Col>
                  <Col>
                    <Button loading={loading} icon={<DollarOutlined />} onClick={handleSettle}>
                      一键结算奖学金
                    </Button>
                  </Col>
                  <Col>
                     <Button icon={<FileExcelOutlined />} onClick={handleExport}>
                       导出 Excel 报表
                     </Button>
                  </Col>
                </Row>
              </Card>
            )}

            <Table 
              dataSource={data} 
              columns={columns} 
              rowKey="StudentID"
              locale={{ emptyText: '暂无数据，请先录入或在 main.py 实现列表接口' }}
            />

            {/* 录入弹窗 */}
            <Modal title="录入成绩" open={isModalOpen} onCancel={() => setIsModalOpen(false)} footer={null}>
              <Form onFinish={handleAddGrade} layout="vertical">
                <Form.Item label="学生学号" name="student_id" required rules={[{ required: true }]}><InputNumber style={{ width: '100%' }} placeholder="例如: 20250001" /></Form.Item>
                <Form.Item label="课程ID" name="course_id" required rules={[{ required: true }]}><InputNumber style={{ width: '100%' }} placeholder="例如: 1" /></Form.Item>
                <Row gutter={16}>
                  <Col span={8}><Form.Item label="平时 (10%)" name="regular"><InputNumber max={100} min={0} style={{ width: '100%' }} /></Form.Item></Col>
                  <Col span={8}><Form.Item label="期中 (30%)" name="midterm"><InputNumber max={100} min={0} style={{ width: '100%' }} /></Form.Item></Col>
                  <Col span={8}><Form.Item label="期末 (60%)" name="final"><InputNumber max={100} min={0} style={{ width: '100%' }} /></Form.Item></Col>
                </Row>
                <Button type="primary" htmlType="submit" block>提交保存</Button>
              </Form>
            </Modal>
          </>
        );
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider theme="light" collapsible>
        <div style={{ height: 64, margin: 16, background: '#f0f2f5', textAlign:'center', lineHeight:'64px', fontWeight:'bold' }}>
           Grade System
        </div>
        <Menu 
          mode="inline" 
          selectedKeys={[currentPage]} 
          onClick={({ key }) => setCurrentPage(key)}
          items={[
            { key: 'grades', icon: <BookOutlined />, label: '成绩管理' },
            { key: 'comprehensive', icon: <TrophyOutlined />, label: '综合测评' },
            ...(user.role === 'Admin' ? [
              { key: 'students', icon: <TeamOutlined />, label: '学生管理' },
              { key: 'courses', icon: <ReadOutlined />, label: '课程管理' }
            ] : []),
            { key: 'test', icon: <BugOutlined />, label: '系统测试' },
            { key: 'profile', icon: <UserOutlined />, label: '个人中心' },
          ]} 
        />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3>欢迎您，{user.role === 'Teacher' ? '老师' : '同学'} (ID: {user.relatedId})</h3>
          <Button type="text" icon={<LogoutOutlined />} href="/login">退出</Button>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
          {renderContent()}
        </Content>
      </Layout>
    </Layout>
  );
}
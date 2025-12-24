import React, { useState, useEffect } from 'react';
import { 
  Card, Table, Button, Modal, Form, Input, message, 
  Row, Col, Space, Select, InputNumber, Popconfirm, Tag
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons';
import api from '../utils/api';

const { Option } = Select;
const { TextArea } = Input;

interface Course {
  CourseID: number;
  CourseCode: string;
  CourseName: string;
  Credits: number;
  Hours: number;
  CourseType: string;
  Department: string;
  Prerequisites: string;
  Description: string;
  Status: string;
  CreatedAt: string;
  UpdatedAt: string;
}

interface CourseManagementProps {
  user?: {
    role: string;
    relatedId: number;
  };
}

const CourseManagement: React.FC<CourseManagementProps> = ({ user }) => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingCourse, setEditingCourse] = useState<Course | null>(null);
  const [form] = Form.useForm();
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  });
  const [searchText, setSearchText] = useState('');

  // 获取课程列表
  const fetchCourses = async (page = 1, size = 20, search = '') => {
    setLoading(true);
    try {
      const response = await api.get('/api/courses/list', {
        params: { page, size, search }
      });
      setCourses(response.data.courses || []);
      setPagination({
        current: page,
        pageSize: size,
        total: response.data.total || 0
      });
    } catch (error) {
      message.error('获取课程列表失败');
      console.error('Error fetching courses:', error);
    } finally {
      setLoading(false);
    }
  };

  // 搜索课程
  const handleSearch = () => {
    fetchCourses(1, pagination.pageSize, searchText);
  };

  // 新增/编辑课程
  const handleSubmit = async (values: any) => {
    try {
      const data = {
        ...values,
        credits: parseFloat(values.credits),
        hours: parseInt(values.hours)
      };

      if (editingCourse) {
        await api.put(`/api/courses/${editingCourse.CourseID}`, data);
        message.success('课程信息更新成功');
      } else {
        await api.post('/api/courses/add', data);
        message.success('课程添加成功');
      }

      setModalVisible(false);
      form.resetFields();
      setEditingCourse(null);
      fetchCourses(pagination.current, pagination.pageSize, searchText);
    } catch (error: any) {
      message.error(error.response?.data?.detail || '操作失败');
      console.error('Error submitting course:', error);
    }
  };

  // 删除课程
  const handleDelete = async (courseId: number) => {
    try {
      await api.delete(`/api/courses/${courseId}`);
      message.success('课程删除成功');
      fetchCourses(pagination.current, pagination.pageSize, searchText);
    } catch (error: any) {
      message.error(error.response?.data?.detail || '删除失败');
      console.error('Error deleting course:', error);
    }
  };

  // 编辑课程
  const handleEdit = (course: Course) => {
    setEditingCourse(course);
    form.setFieldsValue({
      course_code: course.CourseCode,
      course_name: course.CourseName,
      credits: course.Credits,
      hours: course.Hours,
      course_type: course.CourseType,
      department: course.Department,
      prerequisites: course.Prerequisites,
      description: course.Description,
      status: course.Status
    });
    setModalVisible(true);
  };

  // 新增课程
  const handleAdd = () => {
    setEditingCourse(null);
    form.resetFields();
    setModalVisible(true);
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  // 表格列定义
  const columns = [
    {
      title: '课程编号',
      dataIndex: 'CourseCode',
      key: 'CourseCode',
      width: 120,
      render: (code: string) => <strong>{code}</strong>
    },
    {
      title: '课程名称',
      dataIndex: 'CourseName',
      key: 'CourseName',
      width: 200
    },
    {
      title: '学分',
      dataIndex: 'Credits',
      key: 'Credits',
      width: 80,
      render: (credits: number) => <Tag color="blue">{credits}</Tag>
    },
    {
      title: '学时',
      dataIndex: 'Hours',
      key: 'Hours',
      width: 80,
      render: (hours: number) => `${hours}h`
    },
    {
      title: '课程类型',
      dataIndex: 'CourseType',
      key: 'CourseType',
      width: 100,
      render: (type: string) => (
        <Tag color={type === '必修' ? 'red' : 'green'}>{type}</Tag>
      )
    },
    {
      title: '开课院系',
      dataIndex: 'Department',
      key: 'Department',
      width: 120
    },
    {
      title: '先修课程',
      dataIndex: 'Prerequisites',
      key: 'Prerequisites',
      width: 150,
      render: (prerequisites: string) => prerequisites || '-'
    },
    {
      title: '状态',
      dataIndex: 'Status',
      key: 'Status',
      width: 80,
      render: (status: string) => (
        <Tag color={status === '开设' ? 'green' : 'red'}>{status}</Tag>
      )
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_: any, record: Course) => (
        <Space>
          <Button 
            type="link" 
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这门课程吗？"
            onConfirm={() => handleDelete(record.CourseID)}
            okText="确定"
            cancelText="取消"
          >
            <Button 
              type="link" 
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ];

  // 只有管理员可以管理课程信息
  if (user?.role !== 'Admin') {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <h3>权限不足</h3>
          <p>只有管理员可以管理课程信息</p>
        </div>
      </Card>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
          <Col span={8}>
            <Input.Search
              placeholder="搜索课程编号、名称或院系"
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              onSearch={handleSearch}
              enterButton={<SearchOutlined />}
            />
          </Col>
          <Col span={16} style={{ textAlign: 'right' }}>
            <Button 
              type="primary" 
              icon={<PlusOutlined />}
              onClick={handleAdd}
            >
              新增课程
            </Button>
          </Col>
        </Row>

        <Table
          columns={columns}
          dataSource={courses}
          loading={loading}
          rowKey="CourseID"
          pagination={{
            ...pagination,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 条记录`,
            onChange: (page, size) => {
              fetchCourses(page, size, searchText);
            }
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 新增/编辑课程模态框 */}
      <Modal
        title={editingCourse ? '编辑课程信息' : '新增课程'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
          setEditingCourse(null);
        }}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="课程编号"
                name="course_code"
                rules={[
                  { required: true, message: '请输入课程编号' },
                  { pattern: /^[A-Z]+\d+$/, message: '课程编号格式：如CS001' }
                ]}
              >
                <Input placeholder="如: CS001" disabled={!!editingCourse} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="课程名称"
                name="course_name"
                rules={[{ required: true, message: '请输入课程名称' }]}
              >
                <Input placeholder="课程名称" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                label="学分"
                name="credits"
                rules={[
                  { required: true, message: '请输入学分' },
                  { type: 'number', min: 0.5, max: 10, message: '学分范围0.5-10' }
                ]}
              >
                <InputNumber 
                  style={{ width: '100%' }} 
                  step={0.5} 
                  min={0.5} 
                  max={10}
                  placeholder="如: 3.0"
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                label="学时"
                name="hours"
                rules={[
                  { required: true, message: '请输入学时' },
                  { type: 'number', min: 16, max: 200, message: '学时范围16-200' }
                ]}
              >
                <InputNumber 
                  style={{ width: '100%' }} 
                  min={16} 
                  max={200}
                  placeholder="如: 48"
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                label="课程类型"
                name="course_type"
                rules={[{ required: true, message: '请选择课程类型' }]}
              >
                <Select placeholder="选择类型">
                  <Option value="必修">必修</Option>
                  <Option value="选修">选修</Option>
                  <Option value="实践">实践</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item label="开课院系" name="department">
                <Select placeholder="选择院系">
                  <Option value="计算机学院">计算机学院</Option>
                  <Option value="数学学院">数学学院</Option>
                  <Option value="外语学院">外语学院</Option>
                  <Option value="物理学院">物理学院</Option>
                  <Option value="化学学院">化学学院</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item label="状态" name="status">
                <Select placeholder="选择状态">
                  <Option value="开设">开设</Option>
                  <Option value="已停开">已停开</Option>
                  <Option value="筹备中">筹备中</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item label="先修课程" name="prerequisites">
            <Input placeholder="如: 高等数学A, 线性代数" />
          </Form.Item>

          <Form.Item label="课程描述" name="description">
            <TextArea 
              rows={4} 
              placeholder="课程简介和主要内容..."
              maxLength={500}
              showCount
            />
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingCourse ? '更新' : '添加'}
              </Button>
              <Button onClick={() => {
                setModalVisible(false);
                form.resetFields();
                setEditingCourse(null);
              }}>
                取消
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CourseManagement;
import React, { useState, useEffect } from 'react';
import { 
  Card, Table, Button, Modal, Form, Input, message, 
  Row, Col, Space, Select, DatePicker, Popconfirm, Tag
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons';
import api from '../utils/api';
import dayjs from 'dayjs';

const { Option } = Select;

interface Student {
  StudentID: number;
  Name: string;
  Major: string;
  Gender: string;
  Hometown: string;
  Phone: string;
  Email: string;
  EnrollmentDate: string;
  Status: string;
  ClassName: string;
  CreatedAt: string;
  UpdatedAt: string;
}

interface StudentManagementProps {
  user?: {
    role: string;
    relatedId: number;
  };
}

const StudentManagement: React.FC<StudentManagementProps> = ({ user }) => {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingStudent, setEditingStudent] = useState<Student | null>(null);
  const [form] = Form.useForm();
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  });
  const [searchText, setSearchText] = useState('');

  // 获取学生列表
  const fetchStudents = async (page = 1, size = 20, search = '') => {
    setLoading(true);
    try {
      const response = await api.get('/api/students/list', {
        params: { page, size, search }
      });
      setStudents(response.data.students || []);
      setPagination({
        current: page,
        pageSize: size,
        total: response.data.total || 0
      });
    } catch (error) {
      message.error('获取学生列表失败');
      console.error('Error fetching students:', error);
    } finally {
      setLoading(false);
    }
  };

  // 搜索学生
  const handleSearch = () => {
    fetchStudents(1, pagination.pageSize, searchText);
  };

  // 新增/编辑学生
  const handleSubmit = async (values: any) => {
    try {
      const data = {
        ...values,
        student_id: parseInt(values.student_id),
        class_id: parseInt(values.class_id),
        birthdate: values.birthdate ? values.birthdate.format('YYYY-MM-DD') : null,
        enrollment_date: values.enrollment_date ? values.enrollment_date.format('YYYY-MM-DD') : null
      };

      if (editingStudent) {
        await api.put(`/api/students/${editingStudent.StudentID}`, data);
        message.success('学生信息更新成功');
      } else {
        await api.post('/api/students/add', data);
        message.success('学生添加成功');
      }

      setModalVisible(false);
      form.resetFields();
      setEditingStudent(null);
      fetchStudents(pagination.current, pagination.pageSize, searchText);
    } catch (error: any) {
      message.error(error.response?.data?.detail || '操作失败');
      console.error('Error submitting student:', error);
    }
  };

  // 删除学生
  const handleDelete = async (studentId: number) => {
    try {
      await api.delete(`/api/students/${studentId}`);
      message.success('学生删除成功');
      fetchStudents(pagination.current, pagination.pageSize, searchText);
    } catch (error: any) {
      message.error(error.response?.data?.detail || '删除失败');
      console.error('Error deleting student:', error);
    }
  };

  // 编辑学生
  const handleEdit = (student: Student) => {
    setEditingStudent(student);
    form.setFieldsValue({
      student_id: student.StudentID,
      name: student.Name,
      class_id: 1, // 默认班级ID，实际应该从数据中获取
      major: student.Major,
      gender: student.Gender,
      hometown: student.Hometown,
      phone: student.Phone,
      email: student.Email,
      birthdate: student.EnrollmentDate ? dayjs(student.EnrollmentDate) : null,
      enrollment_date: student.EnrollmentDate ? dayjs(student.EnrollmentDate) : null,
      status: student.Status
    });
    setModalVisible(true);
  };

  // 新增学生
  const handleAdd = () => {
    setEditingStudent(null);
    form.resetFields();
    setModalVisible(true);
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  // 表格列定义
  const columns = [
    {
      title: '学号',
      dataIndex: 'StudentID',
      key: 'StudentID',
      width: 120,
      render: (id: number) => <strong>{id}</strong>
    },
    {
      title: '姓名',
      dataIndex: 'Name',
      key: 'Name',
      width: 100
    },
    {
      title: '专业',
      dataIndex: 'Major',
      key: 'Major',
      width: 150
    },
    {
      title: '性别',
      dataIndex: 'Gender',
      key: 'Gender',
      width: 60,
      render: (gender: string) => (
        <Tag color={gender === '男' ? 'blue' : 'pink'}>{gender || '未设置'}</Tag>
      )
    },
    {
      title: '班级',
      dataIndex: 'ClassName',
      key: 'ClassName',
      width: 120
    },
    {
      title: '籍贯',
      dataIndex: 'Hometown',
      key: 'Hometown',
      width: 100
    },
    {
      title: '联系电话',
      dataIndex: 'Phone',
      key: 'Phone',
      width: 120
    },
    {
      title: '邮箱',
      dataIndex: 'Email',
      key: 'Email',
      width: 180
    },
    {
      title: '状态',
      dataIndex: 'Status',
      key: 'Status',
      width: 80,
      render: (status: string) => (
        <Tag color={status === '在读' ? 'green' : 'red'}>{status}</Tag>
      )
    },
    {
      title: '入学日期',
      dataIndex: 'EnrollmentDate',
      key: 'EnrollmentDate',
      width: 100,
      render: (date: string) => date ? dayjs(date).format('YYYY-MM-DD') : '-'
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_: any, record: Student) => (
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
            title="确定要删除这个学生吗？"
            onConfirm={() => handleDelete(record.StudentID)}
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

  // 只有管理员可以管理学生信息
  if (user?.role !== 'Admin') {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: '50px' }}>
          <h3>权限不足</h3>
          <p>只有管理员可以管理学生信息</p>
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
              placeholder="搜索学号、姓名或班级"
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
              新增学生
            </Button>
          </Col>
        </Row>

        <Table
          columns={columns}
          dataSource={students}
          loading={loading}
          rowKey="StudentID"
          pagination={{
            ...pagination,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 条记录`,
            onChange: (page, size) => {
              fetchStudents(page, size, searchText);
            }
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 新增/编辑学生模态框 */}
      <Modal
        title={editingStudent ? '编辑学生信息' : '新增学生'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
          setEditingStudent(null);
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
                label="学号"
                name="student_id"
                rules={[
                  { required: true, message: '请输入学号' },
                  { pattern: /^\d+$/, message: '学号必须是数字' }
                ]}
              >
                <Input placeholder="如: 3124001479" disabled={!!editingStudent} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="姓名"
                name="name"
                rules={[{ required: true, message: '请输入姓名' }]}
              >
                <Input placeholder="学生姓名" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                label="专业"
                name="major"
                rules={[{ required: true, message: '请输入专业' }]}
              >
                <Input placeholder="如: 数据科学与大数据技术" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                label="班级ID"
                name="class_id"
                rules={[{ required: true, message: '请选择班级' }]}
              >
                <Select placeholder="选择班级">
                  <Option value={1}>数据科学与大数据技术2班</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item label="性别" name="gender">
                <Select placeholder="选择性别">
                  <Option value="男">男</Option>
                  <Option value="女">女</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item label="籍贯" name="hometown">
                <Input placeholder="如: 广东省" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item label="联系电话" name="phone">
                <Input placeholder="手机号码" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item label="邮箱" name="email">
                <Input placeholder="电子邮箱" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item label="出生日期" name="birthdate">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item label="入学日期" name="enrollment_date">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item label="状态" name="status">
                <Select placeholder="选择状态">
                  <Option value="在读">在读</Option>
                  <Option value="休学">休学</Option>
                  <Option value="退学">退学</Option>
                  <Option value="毕业">毕业</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit">
                {editingStudent ? '更新' : '添加'}
              </Button>
              <Button onClick={() => {
                setModalVisible(false);
                form.resetFields();
                setEditingStudent(null);
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

export default StudentManagement;
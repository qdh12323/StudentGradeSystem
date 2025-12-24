import React, { useEffect, useMemo, useState } from 'react';
import { Card, Descriptions, Table, Tag, Row, Col, Select, InputNumber, Button, message, Empty, Space, Typography, Alert, Spin } from 'antd';
import api from '../utils/api';
import { UserState } from '../App';

const { Title, Text } = Typography;

interface ComprehensiveEvaluationProps {
  user: UserState;
}

interface RankingItem {
  ClassRank: number;
  StudentName: string;
  TotalScore: number;
  GPA?: number;
  AcademicScore?: number;
  InnovationTotalScore?: number;
  SocialTotalScore?: number;
  CulturalSportsScore?: number;
}

interface BonusDetail {
  Category: string;
  ItemName: string;
  Score: number;
  Description?: string;
}

interface StudentDetail {
  StudentID: number;
  StudentName: string;
  ClassName?: string;
  GradeRank?: number;
  ClassRank?: number;
  GPA?: number;
  AcademicScore?: number;
  InnovationTotalScore?: number;
  SocialTotalScore?: number;
  CulturalSportsScore?: number;
  TotalScore?: number;
  bonus_details?: BonusDetail[];
  [key: string]: any;
}

const YEAR_OPTIONS = ['2024-2025', '2023-2024'];
const SEMESTER_OPTIONS = [1, 2];

export default function ComprehensiveEvaluation({ user }: ComprehensiveEvaluationProps) {
  const [academicYear, setAcademicYear] = useState<string>('2024-2025');
  const [semester, setSemester] = useState<number>(1);
  const [rankings, setRankings] = useState<RankingItem[]>([]);
  const [rankLoading, setRankLoading] = useState(false);
  const [studentDetail, setStudentDetail] = useState<StudentDetail | null>(null);
  const [studentLoading, setStudentLoading] = useState(false);
  const [studentIdToView, setStudentIdToView] = useState<number | null>(user.role === 'Student' ? user.relatedId : null);

  const isStudent = user.role === 'Student';

  const fetchRankings = async () => {
    setRankLoading(true);
    try {
      const res = await api.get('/api/ranking/list', {
        params: { academic_year: academicYear, semester, limit: 200 },
      });
      setRankings(res.data.rankings || []);
    } catch (error: any) {
      message.error(error?.response?.data?.detail || '获取排名失败');
    } finally {
      setRankLoading(false);
    }
  };

  const fetchStudentDetail = async (id?: number | null) => {
    const targetId = id ?? studentIdToView;
    if (!targetId) return;
    setStudentLoading(true);
    try {
      const res = await api.get(`/api/student/${targetId}`, {
        params: { academic_year: academicYear, semester },
      });
      setStudentDetail(res.data);
    } catch (error: any) {
      setStudentDetail(null);
      if (error?.response?.status === 404) {
        message.warning('未找到该学生的综测数据');
      } else {
        message.error(error?.response?.data?.detail || '获取学生综测失败');
      }
    } finally {
      setStudentLoading(false);
    }
  };

  useEffect(() => {
    fetchRankings();
  }, [academicYear, semester]);

  useEffect(() => {
    if (isStudent && user.relatedId) {
      fetchStudentDetail(user.relatedId);
    }
  }, [academicYear, semester, isStudent, user.relatedId]);

  const rankingColumns = useMemo(
    () => [
      { title: '班级排名', dataIndex: 'ClassRank', key: 'ClassRank' },
      { title: '姓名', dataIndex: 'StudentName', key: 'StudentName' },
      { title: '总积分', dataIndex: 'TotalScore', key: 'TotalScore', render: (v: number) => <Tag color={v < 60 ? 'red' : 'green'}>{v}</Tag> },
      { title: '绩点', dataIndex: 'GPA', key: 'GPA' },
      { title: '学业成绩', dataIndex: 'AcademicScore', key: 'AcademicScore' },
      { title: '创新实践', dataIndex: 'InnovationTotalScore', key: 'InnovationTotalScore' },
      { title: '社会实践', dataIndex: 'SocialTotalScore', key: 'SocialTotalScore' },
      { title: '文体实践', dataIndex: 'CulturalSportsScore', key: 'CulturalSportsScore' },
    ],
    []
  );

  const bonusColumns = [
    { title: '类别', dataIndex: 'Category', key: 'Category' },
    { title: '项目', dataIndex: 'ItemName', key: 'ItemName' },
    { title: '分值', dataIndex: 'Score', key: 'Score' },
    { title: '说明', dataIndex: 'Description', key: 'Description' },
  ];

  const filters = (
    <Space wrap style={{ marginBottom: 16 }}>
      <span>学年</span>
      <Select
        value={academicYear}
        style={{ width: 140 }}
        onChange={setAcademicYear}
        options={YEAR_OPTIONS.map((y) => ({ label: y, value: y }))}
      />
      <span>学期</span>
      <Select
        value={semester}
        style={{ width: 120 }}
        onChange={setSemester}
        options={SEMESTER_OPTIONS.map((s) => ({ label: `第${s}学期`, value: s }))}
      />
      {!isStudent && (
        <>
          <span>学生学号</span>
          <InputNumber
            value={studentIdToView ?? undefined}
            onChange={(v) => setStudentIdToView(v ?? null)}
            style={{ width: 180 }}
            placeholder="输入学号"
          />
          <Button type="primary" onClick={() => fetchStudentDetail(studentIdToView)} disabled={!studentIdToView} loading={studentLoading}>
            查询学生
          </Button>
        </>
      )}
    </Space>
  );

  const studentInfoCard = (
    <Card title="个人综测" extra={!isStudent && <Text type="secondary">教师可用学号查询</Text>} style={{ marginBottom: 16 }}>
      {studentLoading ? (
        <div style={{ textAlign: 'center', padding: '24px 0' }}>
          <Spin />
        </div>
      ) : studentDetail ? (
        <>
          <Descriptions column={2} bordered size="small">
            <Descriptions.Item label="姓名">{studentDetail.StudentName}</Descriptions.Item>
            <Descriptions.Item label="学号">{studentDetail.StudentID}</Descriptions.Item>
            <Descriptions.Item label="班级">{studentDetail.ClassName || '-'}</Descriptions.Item>
            <Descriptions.Item label="班级排名">{studentDetail.ClassRank ?? '-'}</Descriptions.Item>
            <Descriptions.Item label="年级排名">{studentDetail.GradeRank ?? '-'}</Descriptions.Item>
            <Descriptions.Item label="绩点">{studentDetail.GPA ?? '-'}</Descriptions.Item>
            <Descriptions.Item label="学业成绩">{studentDetail.AcademicScore ?? '-'}</Descriptions.Item>
            <Descriptions.Item label="创新实践">{studentDetail.InnovationTotalScore ?? '-'}</Descriptions.Item>
            <Descriptions.Item label="社会实践">{studentDetail.SocialTotalScore ?? '-'}</Descriptions.Item>
            <Descriptions.Item label="文体实践">{studentDetail.CulturalSportsScore ?? '-'}</Descriptions.Item>
            <Descriptions.Item label="总积分" span={2}>
              <Tag color={(studentDetail.TotalScore ?? 0) < 60 ? 'red' : 'green'}>{studentDetail.TotalScore ?? '-'}</Tag>
            </Descriptions.Item>
          </Descriptions>

          <Card title="加分明细" size="small" style={{ marginTop: 16 }}>
            {studentDetail.bonus_details && studentDetail.bonus_details.length > 0 ? (
              <Table
                size="small"
                rowKey={(row) => `${row.Category}-${row.ItemName}-${row.Score}`}
                dataSource={studentDetail.bonus_details}
                columns={bonusColumns}
                pagination={false}
              />
            ) : (
              <Empty description="暂无加分记录" />
            )}
          </Card>
        </>
      ) : (
        <Empty description="请选择学号或登录学生账号查看个人综测" />
      )}
    </Card>
  );

  const rankingCard = (
    <Card title="班级/年级综测排名" extra={<Button onClick={fetchRankings} loading={rankLoading}>刷新</Button>}>
      <Table
        dataSource={rankings}
        columns={rankingColumns}
        rowKey={(row) => `${row.ClassRank}-${row.StudentName}`}
        loading={rankLoading}
        pagination={{ pageSize: 10 }}
        locale={{ emptyText: '暂无排名数据，请检查是否已执行排名计算或导入数据' }}
      />
    </Card>
  );

  return (
    <div style={{ padding: 12 }}>
      <Title level={4} style={{ marginBottom: 12 }}>
        综合测评
      </Title>
      <Alert
        type="info"
        showIcon
        style={{ marginBottom: 16 }}
        message="如无法看到综测数据，请确认已运行后端并执行数据库初始化脚本。默认示例数据学年为 2024-2025，第 1 学期。"
      />
      {filters}
      <Row gutter={16}>
        <Col span={isStudent ? 24 : 10}>{studentInfoCard}</Col>
        <Col span={isStudent ? 24 : 14}>{rankingCard}</Col>
      </Row>
    </div>
  );
}

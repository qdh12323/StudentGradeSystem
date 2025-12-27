# 大数据2班管理系统 - 可视化ER图

## 实体关系图 (使用Mermaid语法)

```mermaid
erDiagram
    %% 实体定义
    STUDENTS {
        BIGINT StudentID PK "学号"
        NVARCHAR Name "姓名"
        NVARCHAR Gender "性别"
        DATE Birthdate "出生日期"
        NVARCHAR Hometown "籍贯"
        NVARCHAR IDCard "身份证号"
        NVARCHAR Phone "联系电话"
        NVARCHAR Email "邮箱"
        NVARCHAR Address "家庭住址"
        INT ClassID FK "班级ID"
        DATE EnrollmentDate "入学日期"
        NVARCHAR Status "学生状态"
        DATETIME CreatedAt "创建时间"
        DATETIME UpdatedAt "更新时间"
    }
    
    CLASSES {
        INT ClassID PK "班级ID"
        NVARCHAR ClassName "班级名称"
        NVARCHAR Major "专业"
        INT Grade "年级"
        NVARCHAR Advisor "班主任"
        DATETIME CreatedAt "创建时间"
    }
    
    COURSES {
        INT CourseID PK "课程ID"
        NVARCHAR CourseCode UK "课程编号"
        NVARCHAR CourseName "课程名称"
        DECIMAL Credits "学分"
        INT Hours "学时"
        NVARCHAR CourseType "课程类型"
        NVARCHAR Department "开课院系"
        NVARCHAR Prerequisites "先修课程"
        NTEXT Description "课程描述"
        NVARCHAR Status "课程状态"
        DATETIME CreatedAt "创建时间"
        DATETIME UpdatedAt "更新时间"
    }
    
    COMPREHENSIVE_EVALUATIONS {
        INT EvaluationID PK "评估ID"
        BIGINT StudentID FK "学号"
        NVARCHAR AcademicYear "学年"
        INT Semester "学期"
        DECIMAL PhysicalScore "体测成绩(T)"
        DECIMAL MoralScore "品德表现评价分(D)"
        DECIMAL GPA "绩点"
        DECIMAL AcademicScore "学业成绩考核分(X)"
        DECIMAL InnovationBasicScore "创新实践基本分(C1)"
        DECIMAL InnovationBonusScore "创新实践加分(C2)"
        DECIMAL InnovationTotalScore "创新实践总分(C)"
        DECIMAL StudentWorkScore "学生工作加分(S1)"
        DECIMAL SocialServiceScore "社会服务加分(S2)"
        DECIMAL SocialRewardScore "社会服务奖励加分(S3)"
        DECIMAL SocialTotalScore "社会实践总分(S)"
        DECIMAL CulturalSportsScore "文体实践评分(W)"
        DECIMAL TotalScore "总积分(P)"
        INT ClassRank "班级排名"
        INT GradeRank "年级排名"
        DATETIME CreatedAt "创建时间"
        DATETIME UpdatedAt "更新时间"
    }
    
    BONUS_DETAILS {
        INT DetailID PK "详情ID"
        INT EvaluationID FK "评估ID"
        NVARCHAR Category "加分类别"
        NVARCHAR ItemName "加分项目名称"
        DECIMAL Score "加分分数"
        NVARCHAR Description "详细描述"
        NVARCHAR Evidence "证明材料"
        NVARCHAR Status "审核状态"
        DATETIME CreatedAt "创建时间"
    }
    
    COURSE_OFFERINGS {
        INT OfferingID PK "开设ID"
        INT CourseID FK "课程ID"
        NVARCHAR TeacherName "授课教师"
        NVARCHAR AcademicYear "学年"
        INT Semester "学期"
        NVARCHAR ClassTime "上课时间"
        NVARCHAR Classroom "教室"
        INT MaxStudents "最大选课人数"
        INT CurrentStudents "当前选课人数"
        DATETIME CreatedAt "创建时间"
    }
    
    USERS {
        INT UserID PK "用户ID"
        NVARCHAR Username UK "用户名"
        NVARCHAR PasswordHash "密码哈希"
        NVARCHAR Role "角色"
        BIGINT RelatedID "关联ID"
        DATETIME CreatedAt "创建时间"
    }
    
    %% 关系定义
    CLASSES ||--o{ STUDENTS : "包含"
    STUDENTS ||--o{ COMPREHENSIVE_EVALUATIONS : "参与"
    COMPREHENSIVE_EVALUATIONS ||--o{ BONUS_DETAILS : "包含"
    COURSES ||--o{ COURSE_OFFERINGS : "开设"
    USERS ||--o| STUDENTS : "关联"
```

## 数据库关系图 (简化版)

```mermaid
graph TD
    %% 主要实体
    A[学生 Students<br/>StudentID, Name, ClassID]
    B[班级 Classes<br/>ClassID, ClassName, Major]
    C[课程 Courses<br/>CourseID, CourseCode, CourseName]
    D[综合测评 ComprehensiveEvaluations<br/>EvaluationID, StudentID, TotalScore]
    E[加分详情 BonusDetails<br/>DetailID, EvaluationID, Score]
    F[课程开设 CourseOfferings<br/>OfferingID, CourseID, TeacherName]
    G[用户 Users<br/>UserID, Username, Role]
    
    %% 关系连接
    B -->|1:N| A
    A -->|1:N| D
    D -->|1:N| E
    C -->|1:N| F
    G -.->|关联| A
    
    %% 样式
    classDef entityBox fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef relationBox fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    
    class A,B,C,D,E,F,G entityBox
```

## 综合测评评分体系图

```mermaid
graph LR
    %% 评分组成
    P[总积分 P] --> X[学业成绩考核分 X]
    P --> C[创新实践总分 C]
    P --> S[社会实践总分 S]
    P --> W[文体实践评分 W]
    
    %% 创新实践分解
    C --> C1[创新实践基本分 C1]
    C --> C2[创新实践加分 C2]
    
    %% 社会实践分解
    S --> S1[学生工作加分 S1]
    S --> S2[社会服务加分 S2]
    S --> S3[社会服务奖励加分 S3]
    
    %% 其他基础分
    T[体测成绩 T]
    D[品德表现评价分 D]
    GPA[绩点 GPA]
    
    %% 样式
    classDef totalScore fill:#ffcdd2,stroke:#d32f2f,stroke-width:3px
    classDef mainScore fill:#c8e6c9,stroke:#388e3c,stroke-width:2px
    classDef subScore fill:#fff3e0,stroke:#f57c00,stroke-width:1px
    classDef baseScore fill:#e3f2fd,stroke:#1976d2,stroke-width:1px
    
    class P totalScore
    class X,C,S,W mainScore
    class C1,C2,S1,S2,S3 subScore
    class T,D,GPA baseScore
```

## 用户权限关系图

```mermaid
graph TD
    %% 用户角色
    Admin[管理员 Admin]
    Teacher[教师 Teacher]
    Student[学生 Student]
    
    %% 功能模块
    StudentMgmt[学生信息管理]
    CourseMgmt[课程信息管理]
    EvalMgmt[综测数据管理]
    RankView[排名查看]
    DataExport[数据导出]
    PersonalView[个人信息查看]
    
    %% 权限关系
    Admin --> StudentMgmt
    Admin --> CourseMgmt
    Admin --> EvalMgmt
    Admin --> RankView
    Admin --> DataExport
    Admin --> PersonalView
    
    Teacher --> EvalMgmt
    Teacher --> RankView
    Teacher --> DataExport
    Teacher --> PersonalView
    
    Student --> PersonalView
    Student --> RankView
    
    %% 样式
    classDef adminRole fill:#ffebee,stroke:#c62828,stroke-width:2px
    classDef teacherRole fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef studentRole fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef function fill:#fff9c4,stroke:#f57f17,stroke-width:1px
    
    class Admin adminRole
    class Teacher teacherRole
    class Student studentRole
    class StudentMgmt,CourseMgmt,EvalMgmt,RankView,DataExport,PersonalView function
```

## 数据流程图

```mermaid
flowchart TD
    %% 数据输入
    Start([开始]) --> Login[用户登录]
    Login --> Role{角色判断}
    
    %% 管理员流程
    Role -->|管理员| AdminPanel[管理员面板]
    AdminPanel --> StudentAdd[新增学生]
    AdminPanel --> CourseAdd[新增课程]
    AdminPanel --> EvalAdd[录入综测]
    
    %% 教师流程
    Role -->|教师| TeacherPanel[教师面板]
    TeacherPanel --> EvalManage[综测管理]
    TeacherPanel --> RankCalc[排名计算]
    
    %% 学生流程
    Role -->|学生| StudentPanel[学生面板]
    StudentPanel --> ViewPersonal[查看个人信息]
    StudentPanel --> ViewRank[查看排名前10]
    
    %% 数据处理
    StudentAdd --> DB[(数据库)]
    CourseAdd --> DB
    EvalAdd --> DB
    EvalManage --> DB
    RankCalc --> CalcProc[排名计算存储过程]
    CalcProc --> DB
    
    %% 数据输出
    DB --> Report[生成报表]
    DB --> Export[Excel导出]
    ViewPersonal --> DB
    ViewRank --> DB
    
    %% 样式
    classDef startEnd fill:#c8e6c9,stroke:#4caf50,stroke-width:2px
    classDef process fill:#bbdefb,stroke:#2196f3,stroke-width:2px
    classDef decision fill:#ffcdd2,stroke:#f44336,stroke-width:2px
    classDef database fill:#f3e5f5,stroke:#9c27b0,stroke-width:2px
    
    class Start,Report,Export startEnd
    class Login,AdminPanel,TeacherPanel,StudentPanel,StudentAdd,CourseAdd,EvalAdd,EvalManage,RankCalc,ViewPersonal,ViewRank,CalcProc process
    class Role decision
    class DB database
```

---

**使用说明**:
1. 将以上Mermaid代码复制到支持Mermaid的工具中查看图形化效果
2. 推荐工具: GitHub、GitLab、Typora、VS Code (Mermaid插件)、在线Mermaid编辑器
3. 这些图表可以直接用于答辩PPT中
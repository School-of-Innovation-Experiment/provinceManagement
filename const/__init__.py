# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: const defination
'''

from settings import STATIC_URL, MEDIA_URL, IS_MINZU_SCHOOL, IS_DLUT_SCHOOL

UNDIFINED = "undifined"

# For UserIdentity Table
SCHOOL_USER = "school" # original: student
EXPERT_USER = "expert"
ADMINSTAFF_USER = "adminstaff"
TEACHER_USER = "teacher"
STUDENT_USER = "student"
VISITOR_USER = "visitor"

AUTH_CHOICES = (
    (SCHOOL_USER, u"学院"),
    (EXPERT_USER, u"专家"),
    (ADMINSTAFF_USER, u"省级管理员"),
    (TEACHER_USER, u"指导老师"),
    (STUDENT_USER, u"参赛学生"),
    (VISITOR_USER, u"游客"),
)

INSTITUTE_GRADE = "0"
SCHOOL_GRADE = "1"
EXPERT_GRADE_CHOICES = (
    (INSTITUTE_GRADE, u"院系内项目初审专家"),
    (SCHOOL_GRADE, u"校级以上项目评审专家"),
)
#Project Category
CATE_INNOVATION = "innovation"
CATE_ENTERPRISE = "enterprise"
CATE_ENTERPRISE_EE = "enterprise_ee"
CATE_UN = "undifined"

PROJECT_CATE_CHOICES = (
    (CATE_INNOVATION, u"创新训练"),
    (CATE_ENTERPRISE, u"创业训练"),
    (CATE_ENTERPRISE_EE, u"创业实践"),
    #  (CATE_UN, u"未指定"),
)

#Project_Origin
PROJECT_INNOVATION_ORIGIN_CHOICES = (
    ("0", u"学生自选，学生的积累和兴趣"),
    ("1", u"学生自选，教师的科研项目"),
    ("2", u"教师帮选，教师的科研项目")
)

PROJECT_ENTERPRISE_ORIGIN_CHOICES = (
    ("0", u"前期创新项目成果"),
    ("1", u"导师的科研项目"),
    ("2", u"创新性的课题"),
    ("3", u"已有产品的继续研发"),
    ("4", u"企业的需求"),
    ("5", u"竞赛获奖作品"),
    ("6", u"科技计划资助"),
    ("7", u"其他"),
)
PROJECT_ENTERPRISE_MATURITY_CHOICES = (
    ("0", u"发明专利"),
    ("1", u"实用新型（设计）专利"),
    ("2", u"著作权利"),
    ("3", u"科技成果鉴定"),
    ("4", u"成熟的设想"),
    ("5", u"初步测试成功"),
    ("6", u"其他"),
)

#Project Grade
GRADE_NATION = "nation"
GRADE_PROVINCE = "province"
GRADE_CITY = "city"
GRADE_SCHOOL = "school"
GRADE_INSITUTE = "insitute"
GRADE_UN = "undefined"

PROJECT_GRADE_CHOICES = (
    (GRADE_NATION, u"国家级"),
    (GRADE_PROVINCE, u"省级"),
    (GRADE_CITY, u"市级"),
    (GRADE_SCHOOL, u"校级"),
    (GRADE_INSITUTE, u"学院级"),
    (GRADE_UN, u"未指定"),
)

#Project Review
STATUS_PRESUBMIT = "presubmit"
STATUS_PREREVIEW = "prereview"
STATUS_FINSUBMIT = "finsubmit"
STATUS_FINREVIEW = "finreview"
STATUS_ONGOING = "ongoing"
STATUS_FIRST = "undifined"

PROJECT_STATUS_CHOICES = (
    (STATUS_PRESUBMIT, u'申请提交'),
    (STATUS_PREREVIEW, u'申请评审'),
    (STATUS_FINSUBMIT, u'结题提交'),
    (STATUS_FINREVIEW, u'结题评审'),
    (STATUS_ONGOING, u'正在进行'),
    (STATUS_FIRST, u'初始状态'),
)

OVER_STATUS_NOTOVER = "notover"
OVER_STATUS_OPENCHECK = "opencheck"
OVER_STATUS_MIDCHECK = "midcheck"
OVER_STATUS_FINCHECK = "fincheck"
OVER_STATUS_NORMAL = "normal"
OVER_STATUS_CHOICES = (
    (OVER_STATUS_NOTOVER, u"没有结束"),
    (OVER_STATUS_OPENCHECK, u"开题不通过"),
    (OVER_STATUS_MIDCHECK, u"中期检查不通过"),
    (OVER_STATUS_FINCHECK, u"结题检查不通过"),
    (OVER_STATUS_NORMAL, u"正常结题"),
)

# APP: news
# the following 4 variables are used in foreground,
# so use some meaning words
NEWS_CATEGORY_ANNOUNCEMENT = "announcement"
NEWS_CATEGORY_POLICY = "policy"
NEWS_CATEGORY_OUTSTANDING = "outstanding"
NEWS_CATEGORY_OTHERS = "others"
NEWS_CATEGORY_DOCUMENTS = "documents"
NEWS_CATEGORY_CHOICES = (
    (NEWS_CATEGORY_ANNOUNCEMENT, u"通知公告"),
    (NEWS_CATEGORY_POLICY, u"政策规章"),
    (NEWS_CATEGORY_OUTSTANDING, u"优秀项目"),
    (NEWS_CATEGORY_OTHERS, u"他山之石"),
)
# the max length of news_content
NEWS_MAX_LENGTH = 10000000


# Paginator default Page elements
PAGE_ELEMENTS = 10

# Default img url while img not find
DEFAULT_IMG_URL = STATIC_URL + "/images/no_pic.jpg"

#YEAR
YEAR_CHOICES = tuple([(y, y) for y in range(2000, 2049)])

# adminStaff noticeMessage settings
MESSAGE_EXPERT_HEAD = '__experts__'
MESSAGE_SCHOOL_HEAD = '__schools__'
MESSAGE_STUDENT_HEAD = '__student__'
MESSAGE_TEACHER_HEAD = '__teacher__'
MESSAGE_ALL_HEAD     = '__allmess__'
MESSAGE_ROLE_CHOICES =(
    ('1',u"专家"),
    ('2',u"学院"),
    ('3',u"学生"),
    ('4',u"教师"),
    ('5',u"全部"),
)
# APP student
DEFAULT_NATION = u"汉族"
SEX_MALE = "male"
SEX_FEMALE = "female"
SEX_CHOICES = (
    (SEX_MALE, u"男"),
    (SEX_FEMALE, u"女"),
)

# dlut major
DLUT_MAJOR_CHOICES = (
    ('0', "哲学"),
    ('1', "国际经济与贸易（英语强化）"),
    ('2', "金融学（英语强化）"),
    ('3', "法学"),
    ('4', "思想政治教育"),
    ('5', "汉语言文学"),
    ('6', "汉语言"),
    ('7', "英语"),
    ('8', "日语"),
    ('9', "翻译"),
    ('10', "广播电视新闻学"),
    ('11', "数学与应用数学"),
    ('12', "信息与计算科学"),
    ('13', "应用物理学"),
    ('14', "应用化学"),
    ('15', "生物技术"),
    ('16', "工程力学"),
    ('17', "机械设计制造及其自动化"),
    ('18', "机械设计制造及其自动化（日语强化）"),
    ('19', "机械设计制造及其自动化（国际班）"),
    ('20', "材料成型及控制工程"),
    ('21', "工业设计"),
    ('22', "过程装备与控制工程"),
    ('23', "车辆工程（英语强化）"),
    ('24', "测控技术与仪器"),
    ('25', "材料物理"),
    ('26', "金属材料工程"),
    ('27', "金属材料工程（日语强化）"),
    ('28', "无机非金属材料工程"),
    ('29', "高分子材料与工程"),
    ('30', "功能材料"),
    ('31', "纳米材料与技术"),
    ('32', "能源与动力工程"),
    ('33', "能源与环境系统工程"),
    ('34', "电气工程及其自动化"),
    ('35', "电子信息工程"),
    ('36', "电子信息工程（英语强化）"),
    ('37', "电子科学与技术"),
    ('38', "通信工程"),
    ('39', "光信息科学与技术"),
    ('40', "集成电路设计与集成系统"),
    ('41', "自动化"),
    ('42', "计算机科学与技术"),
    ('43', "计算机科学与技术（日语强化）"),
    ('44', "计算机科学与技术"),
    ('45', "软件工程"),
    ('46', "软件工程"),
    ('47', "软件工程（日语强化）"),
    ('48', "网络工程"),
    ('49', "物联网工程"),
    ('50', "土木工程"),
    ('51', "土木工程（国际班）"),
    ('52', "建筑环境与能源应用工程"),
    ('53', "水利水电工程"),
    ('54', "港口航道与海岸工程"),
    ('55', "化学工程与工艺"),
    ('56', "化学工程与工艺（国际班）"),
    ('57', "制药工程"),
    ('58', "能源化学工程"),
    ('59', "交通工程"),
    ('60', "船舶与海洋工程"),
    ('61', "海洋资源开发技术"),
    ('62', "飞行器设计与工程"),
    ('63', "环境工程"),
    ('64', "环境科学"),
    ('65', "生物医学工程"),
    ('66', "建筑学"),
    ('67', "城乡规划"),
    ('68', "安全工程"),
    ('69', "生物工程"),
    ('70', "信息管理与信息系统"),
    ('71', "工程管理"),
    ('72', "工商管理"),
    ('73', "市场营销"),
    ('74', "人力资源管理"),
    ('75', "公共事业管理"),
    ('76', "物流管理"),
    ('77', "物流工程"),
    ('78', "工业工程"),
    ('79', "雕塑"),
    ('80', "视觉传达设计"),
    ('81', "环境设计"),
    ('82', "生物信息学"),
    ('83', "经济学"),
    ('84', "知识产权"),
    ('85', "环境生态工程"),
    ('86', "商务英语"),
    ('87', "运动康复"),
    ('88', "电子商务"),
)

# minzu major
MINZU_MAJOR_CHOICES = (
    ('1', u"工商管理"),
    ('2', u"经济学"),
    ('3', u"旅游管理"),
    ('4', u"行政管理"),
    ('5', u"市场营销"),
    ('6', u"人力资源管理"),
    ('7', u"机械设计制造及其自动化"),
    ('8', u"工业工程"),
    ('9', u"自动化"),
    ('10', u"测控技术与仪器"),
    ('11', u"车辆工程"),
    ('12', u"化学工程与工艺"),
    ('13', u"应用化学"),
    ('14', u"生物工程"),
    ('15', u"食品科学与工程"),
    ('16', u"食品质量与安全"),
    ('17', u"制药工程"),
    ('18', u"英语"),
    ('19', u"日语"),
    ('20', u"朝鲜语"),
    ('21', u"计算机科学与技术"),
    ('22', u"软件工程"),
    ('23', u"网络工程"),
    ('24', u"土木工程"),
    ('25', u"工程管理"),
    ('26', u"建筑学"),
    ('27', u"建筑环境与能源应用工程"),
    ('28', u"法学"),
    ('29', u"汉语言"),
    ('30', u"新闻学"),
    ('31', u"汉语国际教育（原对外汉语）"),
    ('32', u"信息与计算科学"),
    ('33', u"数学与应用数学"),
    ('34', u"会计学"),
    ('35', u"财务管理"),
    ('36', u"国际经济与贸易"),
    ('37', u"国际商务"),
    ('38', u"电子信息工程"),
    ('39', u"通信工程"),
    ('40', u"物联网工程"),
    ('41', u"生物技术"),
    ('42', u"环境工程"),
    ('43', u"环境科学"),
    ('44', u"功能材料"),
    ('45', u"光电信息科学与工程（原光电子材料与器件与光电子技术科学合并）"),
    ('46', u"视觉传达设计（原艺术设计分设）"),
    ('47', u"环境设计（原艺术设计分设）"),
    ('48', u"产品设计（原艺术设计分设）"),
    ('49', u"动画"),
    ('50', u"工业设计"),
)

if IS_MINZU_SCHOOL: MAJOR_CHOICES = MINZU_MAJOR_CHOICES
if IS_DLUT_SCHOOL: MAJOR_CHOICES = DLUT_MAJOR_CHOICES

# 项目类型团队人员限制
MEMBER_NUM_LIMIT = {
    CATE_INNOVATION: 5,
    # CATE_INNOVATION: 3,
    CATE_ENTERPRISE: 5,
    CATE_ENTERPRISE_EE: 5,
}

# School recommend rate
SCHOOL_RECOMMEND_RATE = 0.3 # 30 %


# Message noticeMessage
TEMPLATE_NOTICE_MESSAGE_MAX = 8
# Progress Record
PROGRESS_RECORD_MAX = 20

# school code
if IS_MINZU_SCHOOL: DUT_code = "12026" # MINZU_code
elif IS_DLUT_SCHOOL: DUT_code = "10141"
# DUT_code = "10141"

EXCEL_TYPE_BASEINFORMATION = "baseinformation"
EXCEL_TYPE_APPLICATIONSCORE = "applicationscore"
EXCEL_TYPE_SUMMARYSHEET_INNOVATE = "summary_innovate"
EXCEL_TYPE_SUMMARYSHEET_ENTREPRENEUSHIP = "summary_entrepreneuship"
EXCEL_TYPE_PROJECTSUMMARY = "projectsummary"
EXCEL_TYPE_CHOICES = (
    (EXCEL_TYPE_BASEINFORMATION, u"基本状态表"),
    (EXCEL_TYPE_APPLICATIONSCORE, u"初期评分表"),
    (EXCEL_TYPE_SUMMARYSHEET_INNOVATE, u"创新项目汇总表"),
    (EXCEL_TYPE_SUMMARYSHEET_ENTREPRENEUSHIP, u"创业项目汇总表"),
    (EXCEL_TYPE_PROJECTSUMMARY,u"项目基本信息汇总表"),
)

FileList={
    'show_applicationwarn' : u"申报书",
    'show_interimchecklist' : u"中期检查表",
    'show_summary' : u"结题验收表",
    'show_projectcompilation' : u"项目汇编",
    'show_scoreapplication' : u"学分申请表",
    'show_opencheck':u'开题报告',
    'show_other':u'其他附件',
} 

# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: const defination
'''

from settings import STATIC_URL, MEDIA_URL

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
GRADE_UN = "undifined"

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


# APP: news


# Paginator default Page elements
PAGE_ELEMENTS = 10

# Default img url while img not find
DEFAULT_IMG_URL = STATIC_URL + "/images/no_pic.jpg"

#YEAR
YEAR_CHOICES = tuple([(y, y) for y in range(2000, 2049)])

# adminStaff noticeMessage settings
MESSAGE_EXPERT_HEAD = '__expert__'
MESSAGE_SCHOOL_HEAD = '__school__'
MESSAGE_STUDENT_HEAD = '__student__'
MESSAGE_TEACHER_HEAD = '__teacher__'
# APP student
# 项目类型团队人员限制
MEMBER_NUM_LIMIT = {
    CATE_INNOVATION: 3,
    CATE_ENTERPRISE: 5,
    CATE_ENTERPRISE_EE: 5,
    }

# School recommend rate
SCHOOL_RECOMMEND_RATE = 0.3 # 30 %

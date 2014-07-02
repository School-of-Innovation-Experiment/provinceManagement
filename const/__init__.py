# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: const defination
'''

from settings import STATIC_URL, MEDIA_URL

UNDIFINED = "undifined"

# For UserIdentity Table
SCHOOL_USER = "schoolstaff"
STUDENT_USER = "student"
EXPERT_USER = "expert"
ADMINSTAFF_USER = "adminstaff"
VISITOR_USER = "visitor"

AUTH_CHOICES = (
    (SCHOOL_USER, u"高校"),
    (EXPERT_USER, u"专家"),
    (ADMINSTAFF_USER, u"省级管理员"),
    (STUDENT_USER, u"参赛团队"),
    (VISITOR_USER, u"游客"),
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
    # (CATE_UN, u"未指定"),
)

#FinancialCategory
FINANCIAL_CATE_A = 'a'
FINANCIAL_CATE_B = 'b'
FINANCIAL_CATE_UN = 'un'

FINANCIAL_CATE_CHOICES = (
    (FINANCIAL_CATE_A, u"甲类"),
    (FINANCIAL_CATE_B, u"乙类"),
    (FINANCIAL_CATE_UN, u"未指定"),
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
GRADE_UN = "undifined"

PROJECT_GRADE_CHOICES = (
    (GRADE_NATION, u"国家级"),
    (GRADE_PROVINCE, u"省级"),
    (GRADE_UN, u"未指定"),
)

#InsituteCategory
INSITUTE_CATEGORY_CHOICES = (
    ("0", u"哲学"),
    ("1", u"经济学"),
    ("2", u"法学"),
    ("3", u"教育学"),
    ("4", u"文学"),
    ("5", u"历史学"),
    ("6", u"理学"),
    ("7", u"工学"),
    ("8", u"农学"),
    ("9", u"医学"),
    ("10", u"管理学"),
    ("11", u"艺术学"),
    ("12", u"全部"),
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

PROJECT_RECOMMEND_CHOICES =(

)


# APP: news
# the following 4 variables are used in foreground,
# so use some meaning words
NEWS_CATEGORY_ANNOUNCEMENT = "announcement"
NEWS_CATEGORY_POLICY = "policy"
NEWS_CATEGORY_DYNAMIC = "dynamic"
NEWS_CATEGORY_OUTSTANDING = "outstanding"
NEWS_CATEGORY_OTHERS = "others"
NEWS_CATEGORY_DOCUMENTS = "documents"
NEWS_CATEGORY_CHOICES = (
    (NEWS_CATEGORY_ANNOUNCEMENT, u"通知公告"),
    (NEWS_CATEGORY_DYNAMIC, u"高校动态"),
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
MESSAGE_EXPERT_HEAD = '__expert__'
MESSAGE_SCHOOL_HEAD = '__school__'

# download file size
DOWNLOAD_BUF_SIZE=262144

MEMBER_NUM_LIMIT = {
    CATE_INNOVATION: 5,
    CATE_ENTERPRISE: 5,
    CATE_ENTERPRISE_EE: 5,
    }
School_Code = {
    '10169':"鞍山师范学院",
    '10167':"渤海大学",
    '11258':"大连大学",
    '13631':"大连东软信息学院",
    '10152':"大连工业大学",
    '10151':"大连海事大学",
    '10158':"大连海洋大学",
    '10150':"大连交通大学",
    '10141':"大连理工大学",
    '13198':"大连理工大学城市学院",
    '12026':"大连民族学院",
    '10172':"大连外国语学院",
    '10161':"大连医科大学",
    '13212':"大连医科大学中山学院",
    '13599':"大连艺术学院",
    '10173':"东北财经大学",
    '10145':"东北大学",
    '11779':"辽东学院",
    '10140':"辽宁大学",
    '10841':"辽宁对外经贸学院",
    '10147':"辽宁工程技术大学",
    '10154':"辽宁工业大学",
    '13610':"辽宁何氏医学院",
    '10146':"辽宁科技大学",
    '11430':"辽宁科技学院",
    '10165':"辽宁师范大学",
    '10148':"辽宁石油化工大学",
    '13583':"辽宁石油化工大学顺华能源学院",
    '10160':"辽宁医学院",
    '10162':"辽宁中医药大学",
    '11035':"沈阳大学",
    '13220':"沈阳城市学院",
    '11632':"沈阳工程学院",
    '10142':"沈阳工业大学",
    '10143':"沈阳航空航天大学",
    '10149':"沈阳化工大学",
    '10153':"沈阳建筑大学",
    '10144':"沈阳理工大学",
    '13201':"沈阳工学院",
    '10157':"沈阳农业大学",
    '10166':"沈阳师范大学",
    '10176':"沈阳体育学院",
    '10163':"沈阳药科大学",
    '10164':"沈阳医学院",
    '10159':"中国医科大学",
}

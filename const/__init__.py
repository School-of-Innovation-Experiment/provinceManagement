# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: const defination
'''

UNDIFINED = "undifined"

# For UserIdentity Table
SCHOOL_USER = "student"
EXPERT_USER = "expert"
ADMINSTAFF_USER = "adminstaff"
VISITOR_USER = "visitor"

AUTH_CHOICES = (
    (SCHOOL_USER, u"高校"),
    (EXPERT_USER, u"专家"),
    (ADMINSTAFF_USER, u"省级管理员"),
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
    (CATE_UN, u"未指定"),
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

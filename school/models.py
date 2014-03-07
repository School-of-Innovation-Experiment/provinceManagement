# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: school's project model, which include pre-submit, final-submit,
      project
'''

import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from const.models import *
from backend.utility import *
from users.models import ExpertProfile, TeacherProfile, StudentProfile, SchoolProfile

from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST
from const import OVER_STATUS_NOTOVER
# from const import YEAR_CHOICES
import datetime

class ProjectSingle(models.Model):
    """
    Every single projects, include basic infomation, it is the base table.
    """
    project_id = models.CharField(max_length=50, primary_key=True,
                                  default=make_uuid,
                                  verbose_name=u"题目唯一ID")

    title = models.CharField(max_length=400, blank=False,
                             verbose_name=u"参赛题目")

    expert = models.ManyToManyField(ExpertProfile, through='Re_Project_Expert')
    adminuser = models.ForeignKey(TeacherProfile, blank=False, null=False, verbose_name=u"指导教师")
    student = models.OneToOneField(StudentProfile, blank=False, null=False, verbose_name=u"参赛学生")

    school = models.ForeignKey(SchoolProfile, blank=False, null=False, verbose_name=u"所属学院")

    project_category = models.ForeignKey(ProjectCategory, verbose_name=u"项目类型",
                                         blank=True, null=True, default=None)
    project_grade = models.ForeignKey(ProjectGrade, verbose_name=u"项目级别",
                                      blank=True, null=True, default=None)
    project_status = models.ForeignKey(ProjectStatus, verbose_name=u"项目状态",
                                       blank=True, null=True,
                                       default=None)
    year = models.IntegerField(blank=False, null=False, max_length=4,
                               default=lambda: datetime.datetime.today().year,
                               verbose_name=u"参加年份")
    recommend = models.BooleanField(null=False, default=False,
                                    verbose_name=u"推荐")
    is_past = models.BooleanField(null=False, default=False,
                                  verbose_name=u"往届项目")
    try:
        default_status = OverStatus.objects.get(status=OVER_STATUS_NOTOVER)
    except:
        default_status = 1
    over_status = models.ForeignKey(OverStatus, verbose_name=u"结束状态",
                                    blank=True, null=True,
                                       default=default_status)
    file_application = models.BooleanField(null=False, default=False,
                                  verbose_name=u"申报书")
    file_opencheck = models.BooleanField(null=False, default=False,
                                verbose_name=u"开题检查表")
    file_interimchecklist = models.BooleanField(null=False, default=False,
                                  verbose_name=u"中期检查表")
    file_summary = models.BooleanField(null=False, default=False,
                                  verbose_name=u"结题验收")
    file_projectcompilation = models.BooleanField(null=False, default=False,
                                  verbose_name=u"项目汇编")
    score_application = models.BooleanField(null=False, default=False,
                                  verbose_name=u"学分申请")
    # is_applicationover = models.BooleanField(null=False, default=False,
    #                               verbose_name=u"申请结束判断")
    funds_total   = models.FloatField(blank=False, verbose_name=u"经费总额",
                                    default=0)
    funds_remain  = models.FloatField(blank=False, verbose_name=u"经费余额",
                                    default=0)
    project_code = models.CharField(blank=False, null=True, max_length=14, verbose_name=u"项目申报编号")
    project_unique_code = models.CharField(blank=True, null=True, default='',
                                           max_length=14, verbose_name=u"项目编号")
    class Meta:
        verbose_name = "参赛项目"
        verbose_name_plural = "参赛项目"

    def __unicode__(self):
        return self.title


class Project_Is_Assigned(models.Model):
    school = models.OneToOneField(SchoolProfile,
                               blank = True, null=True, default=None)
    is_assigned = models.BooleanField(default=False)
    is_assigned_in_presubmit = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"项目分配判断"
        verbose_name_plural = u"项目分配判断"


class Re_Project_Expert(models.Model):
    project = models.ForeignKey(ProjectSingle)
    expert = models.ForeignKey(ExpertProfile)
    is_assign_by_adminStaff = models.BooleanField(default=False, blank=False, null=False)
    comments = models.TextField(blank=True, verbose_name="评价")
    score_significant = models.FloatField(blank=False, verbose_name=u"项目选题意义",
                                          default=0)
    score_value = models.FloatField(blank=False, verbose_name=u"科技研究价值",
                                    default=0)
    score_innovation = models.FloatField(blank=False, verbose_name="项目创新之处",
                                         default=0)
    score_practice = models.FloatField(blank=False, verbose_name="项目可行性",
                                       default=0)
    score_achievement = models.FloatField(blank=False, verbose_name=u"预期成果",
                                          default=0)
    score_capacity = models.FloatField(blank=False, verbose_name=u"指导教师科研能力",
                                       default=0)

    class Meta:
        #Here, we use together unique key, otherwise the one project will be
        #reviewed by one expert twice!
        unique_together=(('project', 'expert', 'is_assign_by_adminStaff',), )
        verbose_name = "项目审核分配"
        verbose_name_plural = "项目审核分配"


class Teacher_Enterprise(models.Model):
    """
    Enterprise teacher for Enterprise Project
    """
    name = models.CharField(blank=True, null=True, max_length=100, default="",
                            verbose_name=u"姓名")
    telephone = models.CharField(blank=True, null=True, max_length=20, default="",
                                 verbose_name=u"联系电话")
    titles = models.CharField(blank=True, null=True, max_length=20, default="",
                              verbose_name=u"职称")
    jobs = models.CharField(max_length=100, blank=True, null=True, default="",
                            verbose_name=u"工作单位")

    class Meta:
        verbose_name = "企业导师"
        verbose_name_plural = "企业导师"

    def __unicode__(self):
        return unicode(self.name) or u'未命名'

class PreSubmit(models.Model):
    """
    inheribit table, which use ProjectSingle to show pre-submit content
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="初审报告唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    original = models.ForeignKey(ProjectOrigin, blank=False, null=True,
                                 verbose_name=u"项目来源")
    background = models.TextField(blank=False, null=True, verbose_name="项目背景及研究意义")
    key_notes = models.TextField(blank=False, null=True,
                                 verbose_name="研究内容和拟解决的关键问题")
    innovation = models.TextField(blank=False, null=True, verbose_name="项目创新之处")
    progress_plan = models.TextField(blank=False, null=True, verbose_name="项目进度安排")
    funds_plan = models.TextField(blank=False, null=True, verbose_name="项目经费预算")
    pre_results = models.TextField(blank=False, null=True, verbose_name="预期研究成果")
    inspector_comments = models.TextField(blank=True, null=True,
                                          verbose_name="指导教师意见")
    instutite_comments = models.TextField(blank=True, null=True,
                                       verbose_name="学部学院评审意见")
    school_comments = models.TextField(blank=True, null=True,
                                       verbose_name="学校评审意见")

    class Meta:
        verbose_name = "项目申报书"
        verbose_name_plural = "项目申报书"

    def __unicode__(self):
        return self.project_id.title

class PreSubmitEnterprise(models.Model):
    """
    inheribit table, which use ProjectSingle to show pre-submit content for Enterprise project
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="初审报告唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    original = models.ForeignKey(ProjectEnterpriseOrigin, blank=False, null=True,
                                 verbose_name=u"项目来源")
    maturity = models.ForeignKey(ProjectEnterpriseMaturity, blank=False, null=True,
                                 verbose_name=u"项目技术成熟度")
    enterpriseTeacher = models.OneToOneField(Teacher_Enterprise, blank=False, null=False,
                                          verbose_name=u"企业导师")
    background = models.TextField(blank=False, null=True, verbose_name=u"创业团队介绍")
    innovation = models.TextField(blank=False, null=True, verbose_name=u"项目的基本情况及创新内容")
    industry = models.TextField(blank=False, null=True, verbose_name=u"行业及市场前景")
    product = models.TextField(blank=False, null=True, verbose_name=u"产品制造")
    funds_plan = models.TextField(blank=False, null=True, verbose_name=u"项目投资预算及融资计划")
    operating_mode = models.TextField(blank=False, null=True, verbose_name=u"项目运营模式")
    risk_management = models.TextField(blank=False, null=True, verbose_name=u"项目风险预测及应对措施")
    financial_pred = models.TextField(blank=False, null=True, verbose_name=u"财务预测")
    inspector_comments = models.TextField(blank=True, null=True,
                                          verbose_name="指导教师意见")
    instutite_comments = models.TextField(blank=True, null=True,
                                       verbose_name="学部学院评审意见")
    school_comments = models.TextField(blank=True, null=True,
                                       verbose_name="学校评审意见")

    class Meta:
        verbose_name = "创业项目申报书"
        verbose_name_plural = "创业项目申报书"

    def __unicode__(self):
        return self.project_id.title


class OpenSubmit(models.Model):
    """
    Mid submit
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="开题检查表唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    content = models.TextField(blank=False, null=True,
                               verbose_name="研究内容")
    study_achievement = models.TextField(blank=False, null=True,
                                           verbose_name="前期研究和成果")
    next_plan_target = models.TextField(blank=False, null=True,
                                 verbose_name="下一阶段计划及目标")
    inspector_comments = models.TextField(blank=True, null=True,
                                          verbose_name="指导教师意见")

    class Meta:
        verbose_name = "项目开题检查表"
        verbose_name_plural = "项目开题检查表"

    def __unicode__(self):
        return self.project_id.title


class MidSubmit(models.Model):
    """
    Mid submit
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="中期检查表唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    process = models.TextField(blank=False, null=True,
                               verbose_name="项目进展情况")
    achievement_summary = models.TextField(blank=False, null=True,
                                           verbose_name="研究成果概述")
    next_plan = models.TextField(blank=False, null=True,
                                 verbose_name="下一阶段工作计划")
    achievement = models.TextField(blank=False, null=True,
                                   verbose_name="主要成果")
    inspector_comments = models.TextField(blank=True, null=True,
                                          verbose_name="指导教师意见")

    class Meta:
        verbose_name = "项目中期检查表"
        verbose_name_plural = "项目中期检查表"

    def __unicode__(self):
        return self.project_id.title


class FinalSubmit(models.Model):
    """
    inheribit table, which use ProjectSingle to show final-submit content
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="结题报告唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    achievement_fashion = models.CharField(max_length=200, blank=True, null=True,
                                           verbose_name="成果形式")
    achievement_summary = models.TextField(blank=False, null=True,
                                           verbose_name="研究成果概述")
    inspector_comments = models.TextField(blank=False, null=True,
                                          verbose_name="指导教师推荐语")
    school_comments = models.TextField(blank=False, null=True,
                                       verbose_name="学校推荐语")

    # tech_competitions = models.TextField(blank=True, null=True, verbose_name="科技竞赛成果")
    # patents = models.TextField(blank=True, null=True, verbose_name="发明专利成果")
    # papers = models.TextField(blank=True, null=True, verbose_name="发表论文")
    # achievement_objects = models.TextField(blank=True, null=True, verbose_name="实物成果")

    class Meta:
        verbose_name = "项目结题报告"
        verbose_name_plural = "项目结题报告"

    def __unicode__(self):
        return self.project_id.title

class TechCompetition(models.Model):
    """
    Technology competition achievement, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="科技竞赛成果唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name="竞赛作品名称")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name="参加人")
    competition_name = models.CharField(max_length=100, blank=False,
                                        verbose_name="获奖名称")
    competition_grade = models.CharField(max_length=20, blank=False,
                                         verbose_name="获奖等级")

    class Meta:
        verbose_name = "科技竞赛"
        verbose_name_plural = "科技竞赛"

    def __unicode__(self):
        return self.project_id.project_id.title


class Patents(models.Model):
    """
    Patent achievement, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="发明专利唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name="专利题名")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name="专利申请者")
    number = models.CharField(max_length=100, blank=False,
                              verbose_name="专利号")
    finish_date = models.DateField(blank=False,
                                   verbose_name="批准时间")

    class Meta:
        verbose_name = "发明专利"
        verbose_name_plural = "发明专利"

    def __unicode__(self):
        return self.project_id.project_id.title


class Papers(models.Model):
    """
    Papers achievement, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="学术论文成果唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name="名称")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name="参加人")
    publication = models.CharField(max_length=100, blank=False,
                                   verbose_name="期刊期数")
    finish_date = models.DateField(blank=False,
                                   verbose_name="发表时间")

    class Meta:
        verbose_name = "学术论文"
        verbose_name_plural = "学术论文"

    def __unicode__(self):
        return self.project_id.project_id.title


class AchievementObjects(models.Model):
    """
    Achievement Objects, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name="实物成果唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name="名称")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name="参加人")
    finish_date = models.DateField(blank=False,
                                   verbose_name="完成时间")
    comments = models.TextField(blank=True, verbose_name="备注")

    class Meta:
        verbose_name = "实物"
        verbose_name_plural = "实物"

    def __unicode__(self):
        return self.project_id.project_id.title

class UploadedFiles(models.Model):
    """
    content files upload, which include images, and pdf
    """
    file_id = models.CharField(max_length=50,
                               primary_key=True, default=lambda:str(uuid.uuid4()),
                               verbose_name="文件上传唯一ID")
    project_id = models.ForeignKey(ProjectSingle)
    name = models.CharField(max_length=100, blank=False,
                            verbose_name="文件名称")
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH +"/%Y/%m/%d",
                                verbose_name="文件对象")
    uploadtime = models.DateTimeField(blank=True, null=True,
                                      verbose_name="上传时间")
    file_size = models.CharField(max_length=50, blank=True, null=True,
                                 default=None, verbose_name="文件大小")
    file_type = models.CharField(max_length=50, blank=True, null=True,
                                 default=None, verbose_name="文件类型")

    class Meta:
        verbose_name = "文件上传"
        verbose_name_plural = "文件上传"

    def __unicode__(self):
        return self.project_id.title
    def file_name(self):
        return os.path.basename(self.file_obj.name)


class TeacherProjectPerLimits(models.Model):
    """
    Project apply number limits
    """
    teacher = models.OneToOneField(TeacherProfile, verbose_name="指导教师")
    number = models.IntegerField(blank=False, verbose_name="申请数量上限")

    class Meta:
        verbose_name = "指导教师申请数量限制"
        verbose_name_plural = "指导教师申请数量限制"

    def __unicode__(self):
        return self.teacher.userid.email + ":" +  str(self.number)

class ProjectFinishControl(models.Model):
    """
    Project is_over control
    """
    userid = models.ForeignKey(User)
    project_year = models.IntegerField(blank=False,max_length=4,
                               verbose_name=u"项目年份")
    class Meta:
        verbose_name = "结题项目年份"
        verbose_name_plural = "结题项目年份"

    def __unicode__(self):
        return str(self.project_year)

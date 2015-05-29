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
from users.models import ExpertProfile, StudentProfile, ProjectOrigin, ProjectEnterpriseOrigin, ProjectEnterpriseMaturity

from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST
import datetime

class ShowProjectSingle(models.Model):
    project_id = models.CharField(max_length=50, primary_key=True,
                                  default=make_uuid,
                                  verbose_name=u"题目唯一ID")
    title = models.CharField(max_length=400, blank=False, verbose_name=u"参赛题目")
    school = models.ForeignKey(SchoolDict, blank=True, null=True, default=None)
    teacher = models.CharField(max_length=50, blank=False, verbose_name=u"指导教师")
    members = models.CharField(max_length=400, blank=False,
                               verbose_name=u"团队成员")
    keywords = models.CharField(blank=True, max_length=300,
                                verbose_name=u"关键字")
    background = models.TextField(blank=False, null=True, verbose_name=u"项目背景")
    result_overview = models.TextField(blank=False, null=True,verbose_name=u"成果概述")
    class Meta:
        verbose_name = u"展示项目"
        verbose_name_plural = u"展示项目"

    def __unicode__(self):
        return self.title

class ShowFiles(models.Model):
    """
    content files upload, which include images, and pdf
    """
    file_id = models.CharField(max_length=50,
                               primary_key=True, default=lambda:str(uuid.uuid4()),
                               verbose_name=u"文件上传唯一ID")
    project_id = models.ForeignKey(ShowProjectSingle)
    name = models.CharField(max_length=100, blank=False,
                            verbose_name=u"文件名称")
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH +"/%Y/%m/%d",
                                verbose_name=u"文件对象")
    file_type = models.CharField(max_length=50, blank=True, null=True,
                                 default=None, verbose_name=u"文件类型")

    class Meta:
        verbose_name = u"展示附件"
        verbose_name_plural = u"展示附件"

    def __unicode__(self):
        return self.project_id.title
    def file_name(self):
        return os.path.basename(self.file_obj.name)
 
class ProjectSingle(models.Model):
    """
    Every single projects, include basic infomation, it is the base table.
    """
    project_id = models.CharField(max_length=50, primary_key=True,
                                  default=make_uuid,
                                  verbose_name=u"题目唯一ID")
    title = models.CharField(max_length=400, blank=False, verbose_name=u"参赛题目")

    expert = models.ManyToManyField(ExpertProfile, through='Re_Project_Expert')
    adminuser = models.ForeignKey(User)
    student = models.OneToOneField(StudentProfile)
    school = models.ForeignKey(SchoolDict, blank=True, null=True, default=None)
    project_category = models.ForeignKey(ProjectCategory, blank=True, null=True, default=None)
    financial_category = models.ForeignKey(FinancialCategory, blank=True, null=True, default=None)
    insitute = models.ForeignKey(InsituteCategory,
                                 blank=False, null=True, default=None,
                                 verbose_name=u"学院学科")
    project_grade = models.ForeignKey(ProjectGrade,
                                      blank=True, null=True, default=None)
    project_status = models.ForeignKey(ProjectStatus,
                                       blank=True, null=True,
                                       default=None)
    email = models.EmailField(verbose_name=u"电子邮件")
    telephone = models.CharField(max_length=20, blank=True,
                                 verbose_name=u"联系方式")
    inspector = models.CharField(max_length=200, blank=False,
                                 verbose_name=u"指导教师")
    inspector_title = models.CharField(blank=False,max_length=10,
                                       verbose_name=u"指导老师职称")
    members = models.CharField(max_length=400, blank=False,
                               verbose_name=u"团队成员")
    im = models.CharField(max_length=50, blank=False, verbose_name=u"QQ")
    #choices=YEAR_CHOICES,
    year = models.IntegerField(blank=False, null=False, max_length=4,
                               default=lambda: datetime.datetime.today().year,
                               verbose_name="参赛年份")
    is_past = models.BooleanField(null=False, blank=True, default=False,
                                  verbose_name=u"往届项目")
    is_over = models.BooleanField(null=False, blank=True, default=False,
                                  verbose_name=u"是否结束")
    keywords = models.CharField(blank=True, max_length=300,
                                verbose_name=u"关键字")
    project_code = models.CharField(blank=False, null=True, max_length=20, verbose_name=u"项目编号")
    project_recommend_status = models.ForeignKey(ProjectRecommendStatus, verbose_name=u"项目推荐状态",
                                       blank=True, null=True,
                                       default=None)
    class Meta:
        verbose_name = u"参赛项目"
        verbose_name_plural = u"参赛项目"

    def __unicode__(self):
        return self.title


class Project_Is_Assigned(models.Model):
    insitute = models.ForeignKey(InsituteCategory,
                                blank=True, null=True, default=None
                                )
    is_assigned = models.BooleanField(default=False)
    class Meta:
        verbose_name = u"项目分配判断"
        verbose_name_plural = u"项目分配判断"

    def __unicode__(self):
        return self.insitute.__unicode__() + (u"已分配" if self.is_assigned else u"未分配")


class Re_Project_Expert(models.Model):
    project = models.ForeignKey(ProjectSingle)
    expert = models.ForeignKey(ExpertProfile)
    comments = models.TextField(blank=True, verbose_name=u"评价")
    score_significant = models.FloatField(blank=False, verbose_name=u"项目选题意义",
                                          default=0)
    score_value = models.FloatField(blank=False, verbose_name=u"科技研究价值",
                                    default=0)
    score_innovation = models.FloatField(blank=False, verbose_name=u"项目创新之处",
                                         default=0)
    score_practice = models.FloatField(blank=False, verbose_name=u"项目可行性",
                                       default=0)
    score_achievement = models.FloatField(blank=False, verbose_name=u"预期成果",
                                          default=0)
    score_capacity = models.FloatField(blank=False, verbose_name=u"指导教师科研能力",
                                       default=0)
    pass_p = models.BooleanField(default=False, verbose_name=u"是否通过")
    class Meta:
        #Here, we use together unique key, otherwise the one project will be
        #reviewed by one expert twice!
        unique_together=(('project', 'expert'), )
        verbose_name = u"项目审核分配"
        verbose_name_plural = u"项目审核分配"

class Teacher_Enterprise(models.Model):
    """
    Enterprise teacher for Enterprise Project
    """
    name = models.CharField(blank=True, null=True, max_length=100,
                            verbose_name=u"姓名")
    telephone = models.CharField(blank=True, null=True, max_length=20,
                                 verbose_name=u"联系电话")
    titles = models.CharField(blank=True, null=True, max_length=20,
                              verbose_name=u"职称")
    jobs = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=u"工作单位")

    class Meta:
        verbose_name = u"企业导师"
        verbose_name_plural = u"企业导师"

    def __unicode__(self):
        return self.name


class PreSubmit(models.Model):
    """
    inheribit table, which use ProjectSingle to show pre-submit content
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=make_uuid,
                                  verbose_name=u"初审报告唯一ID")
    project_id = models.ForeignKey(ProjectSingle)
    original = models.ForeignKey(ProjectOrigin, blank=False, null=True,
                                verbose_name=u"题目来源")

    proj_introduction = models.TextField(blank=False, null=True,
                                         verbose_name=u"项目简介")
    background = models.TextField(blank=False, null=True, verbose_name=u"项目背景及研究意义")
    key_notes = models.TextField(blank=False, null=True,
                                 verbose_name=u"研究内容和拟解决的关键问题")
    innovation = models.TextField(blank=False, null=True, verbose_name=u"项目创新之处")
    progress_plan = models.TextField(blank=False, null=True, verbose_name=u"项目进度安排")
    funds_plan = models.TextField(blank=False, null=True, verbose_name=u"项目经费预算")
    pre_results = models.TextField(blank=False, null=True, verbose_name=u"预期研究成果")
    inspector_comments = models.TextField(blank=True, null=True,
                                          verbose_name=u"指导教师推荐语")
    school_comments = models.TextField(blank=True, null=True,
                                       verbose_name=u"学校推荐语")
    is_audited = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"项目申请书"
        verbose_name_plural = u"项目申请书"

    def __unicode__(self):
        return self.project_id.title

class PreSubmitEnterprise(models.Model):
    """
    inheribit table, which use ProjectSingle to show pre-submit content for Enterprise project
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name=u"初审报告唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    original = models.ForeignKey(ProjectEnterpriseOrigin, blank=False, null=True,
                                 verbose_name=u"项目来源")

    proj_introduction = models.TextField(blank=False, null=True, 
                                         verbose_name=u"项目简介")
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
                                          verbose_name=u"指导教师意见")
    school_comments = models.TextField(blank=True, null=True,
                                       verbose_name=u"学校评审意见")
    is_audited = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"创业项目申请书"
        verbose_name_plural = u"创业项目申请书"

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
    is_audited = models.BooleanField(default=False)

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
                                  verbose_name=u"结题报告唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    achievement_fashion = models.CharField(max_length=200, blank=True, null=True,
                                           verbose_name=u"成果形式")
    achievement_summary = models.TextField(blank=False, null=True,
                                           verbose_name=u"研究成果概述")
    inspector_comments = models.TextField(blank=True, null=True,
                                          verbose_name=u"指导教师推荐语")
    school_comments = models.TextField(blank=True, null=True,
                                       verbose_name=u"学校推荐语")
    is_audited = models.BooleanField(default=False)

    class Meta:
        verbose_name = u"项目结题报告"
        verbose_name_plural = u"项目结题报告"

    def __unicode__(self):
        return self.project_id.title

class TechCompetition(models.Model):
    """
    Technology competition achievement, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name=u"科技竞赛成果唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name=u"竞赛作品名称")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name=u"参加人")
    competition_name = models.CharField(max_length=100, blank=False,
                                        verbose_name=u"获奖名称")
    competition_grade = models.CharField(max_length=20, blank=False,
                                         verbose_name=u"获奖等级")

    class Meta:
        verbose_name = u"科技竞赛"
        verbose_name_plural = u"科技竞赛"

    def __unicode__(self):
        return self.project_id.project_id.title


class Patents(models.Model):
    """
    Patent achievement, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name=u"发明专利唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name=u"专利题名")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name=u"专利申请者")
    number = models.CharField(max_length=100, blank=False,
                              verbose_name=u"专利号")
    finish_date = models.DateField(blank=False,
                                   verbose_name=u"批准时间")

    class Meta:
        verbose_name = u"发明专利"
        verbose_name_plural = u"发明专利"

    def __unicode__(self):
        return self.project_id.project_id.title


class Papers(models.Model):
    """
    Papers achievement, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name=u"学术论文成果唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name=u"名称")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name=u"参加人")
    publication = models.CharField(max_length=100, blank=False,
                                   verbose_name=u"期刊期数")
    finish_date = models.DateField(blank=False,
                                   verbose_name=u"发表时间")

    class Meta:
        verbose_name = u"学术论文"
        verbose_name_plural = u"学术论文"

    def __unicode__(self):
        return self.project_id.project_id.title


class AchievementObjects(models.Model):
    """
    Achievement Objects, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50, blank=False, unique=True,
                                  primary_key=True, default=lambda: str(uuid.uuid4()),
                                  verbose_name=u"实物成果唯一ID")
    project_id = models.ForeignKey(FinalSubmit)
    title = models.CharField(max_length=100, blank=False,
                             verbose_name=u"名称")
    members = models.CharField(max_length=100, blank=False,
                               verbose_name=u"参加人")
    finish_date = models.DateField(blank=False,
                                   verbose_name=u"完成时间")
    comments = models.TextField(blank=True, verbose_name=u"备注")

    class Meta:
        verbose_name = u"实物"
        verbose_name_plural = u"实物"

    def __unicode__(self):
        return self.project_id.project_id.title

class UploadedFiles(models.Model):
    """
    content files upload, which include images, and pdf
    """
    file_id = models.CharField(max_length=50,
                               primary_key=True, default=lambda:str(uuid.uuid4()),
                               verbose_name=u"文件上传唯一ID")
    project_id = models.ForeignKey(ProjectSingle)
    name = models.CharField(max_length=100, blank=False,
                            verbose_name=u"文件名称")
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH +"/%Y/%m/%d",
                                verbose_name=u"文件对象")
    uploadtime = models.DateTimeField(blank=True, null=True,
                                      verbose_name=u"上传时间")
    file_size = models.CharField(max_length=50, blank=True, null=True,
                                 default=None, verbose_name=u"文件大小")
    file_type = models.CharField(max_length=50, blank=True, null=True,
                                 default=None, verbose_name=u"文件类型")

    class Meta:
        verbose_name = u"文件上传"
        verbose_name_plural = u"文件上传"

    def __unicode__(self):
        return self.project_id.title
    def file_name(self):
        return os.path.basename(self.file_obj.name)

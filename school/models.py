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
from users.models import ExpertProfile

from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST
from const import YEAR_CHOICES
import datetime

class ProjectSingle(models.Model):
    """
    Every single projects, include basic infomation, it is the base table.
    """
    project_id = models.CharField(max_length=50, primary_key=True,
                                  default=make_uuid,
                                  verbose_name="题目唯一ID")

    title = models.CharField(max_length=400, blank=False,
                             verbose_name="参赛题目")

    expert = models.ManyToManyField(ExpertProfile, through='Re_Project_Expert')
    adminuser = models.ForeignKey(User)
    school = models.ForeignKey(SchoolDict,
                               blank=True, null=True, default=None)
    project_category = models.ForeignKey(ProjectCategory,
                                         blank=True, null=True, default=None)
    insitute = models.ForeignKey(InsituteCategory,
                                 blank=True, null=True, default=None,
                                 verbose_name="所属学院")
    project_grade = models.ForeignKey(ProjectGrade,
                                      blank=True, null=True, default=None)
    project_status = models.ForeignKey(ProjectStatus,
                                       blank=True, null=True,
                                       default=None)
    email = models.EmailField(verbose_name="电子邮件")
    telephone = models.CharField(max_length=20, blank=True,
                                 verbose_name="联系方式")
    inspector = models.CharField(max_length=200, blank=False,
                                 verbose_name="指导教师")
    members = models.CharField(max_length=400, blank=False,
                               verbose_name="团队成员")
    im = models.CharField(max_length=50, blank=False, verbose_name="社交")
    year = models.IntegerField(blank=False, null=False, max_length=4,
                               choices=YEAR_CHOICES, default=lambda:\
                               datetime.datetime.today().year,
                               verbose_name="参加年份")

    class Meta:
        verbose_name = "参赛项目"
        verbose_name_plural = "参赛项目"

    def __unicode__(self):
        return self.title


class Project_Is_Assigned(models.Model):
    insitute = models.ForeignKey(InsituteCategory,
                                blank=True, null=True, default=None
                                )
    is_assigned = models.BooleanField(default=False)


class Re_Project_Expert(models.Model):
    project = models.ForeignKey(ProjectSingle)
    expert = models.ForeignKey(ExpertProfile)
    comments = models.TextField(blank=True, verbose_name="评价")
    score_innovation = models.FloatField(blank=False, verbose_name="创新性",
                                           default=0)
    score_practice = models.FloatField(blank=False, verbose_name="实用性",
                                         default=0)
    score_funny = models.FloatField(blank=False, verbose_name="趣味性",
                                      default=0)

    class Meta:
        #Here, we use together unique key, otherwise the one project will be
        #reviewed by one expert twice!
        unique_together=(('project', 'expert'), )
        verbose_name = "项目审核分配"
        verbose_name_plural = "项目审核分配"

    def __unicode__(self):
        return "%s %s" % (self.project, self.expert)


class PreSubmit(models.Model):
    """
    inheribit table, which use ProjectSingle to show pre-submit content
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=str(uuid.uuid4()),
                                  verbose_name="初审报告唯一ID")
    project_id = models.ForeignKey(ProjectSingle)

    original = models.CharField(max_length=200, blank=False, null=True,
                                verbose_name="题目来源")
    background = models.TextField(blank=False, null=True, verbose_name="项目背景及研究意义")
    key_notes = models.TextField(blank=False, null=True,
                                 verbose_name="研究内容和拟解决的关键问题")
    innovation = models.TextField(blank=False, null=True, verbose_name="项目创新之处")
    progress_plan = models.TextField(blank=False, null=True, verbose_name="项目进度安排")
    funds_plan = models.TextField(blank=False, null=True, verbose_name="项目经费预算")
    pre_results = models.TextField(blank=False, null=True, verbose_name="预期研究成果")
    inspector_comments = models.TextField(blank=False, null=True,
                                          verbose_name="指导教师推荐语")
    school_comments = models.TextField(blank=False, null=True,
                                       verbose_name="学校推荐语")

    class Meta:
        verbose_name = "项目申请书"
        verbose_name_plural = "项目申请书"

    def __unicode__(self):
        return self.project_id.title


class FinalSubmit(models.Model):
    """
    inheribit table, which use ProjectSingle to show final-submit content
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=str(uuid.uuid4()),
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
    tech_competitions = models.TextField(blank=True, null=True,
                                         verbose_name="科技竞赛成果")
    patents = models.TextField(blank=True, null=True,
                               verbose_name="发明专利成果")
    papers = models.TextField(blank=True, null=True,
                              verbose_name="发表论文")
    achievement_objects = models.TextField(blank=True, null=True,
                                           verbose_name="实物成果")

    class Meta:
        verbose_name = "项目结题报告"
        verbose_name_plural = "项目结题报告"

    def __unicode__(self):
        return self.project_id.title

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

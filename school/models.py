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


class ProjectSingle(models.Model):
    """
    Every single projects, include basic infomation, it is the base table.
    """
    project_id = models.CharField(max_length=50, primary_key=True,
                                  default=str(uuid.uuid4()),
                                  verbose_name="题目唯一ID")

    title = models.CharField(max_length=400, blank=False,
                             verbose_name="参赛题目")

    adminuser = models.ForeignKey(User)
    school = models.ForeignKey(SchoolDict)
    project_category = models.ForeignKey(ProjectCategory)
    insitute = models.ForeignKey(InsituteCategory)
    project_grade = models.ForeignKey(ProjectGrade)
    project_status = models.ForeignKey(ProjectStatus)
    email = models.EmailField(verbose_name="电子邮件")
    telephone = models.CharField(max_length=20, blank=True,
                                 verbose_name="联系方式")
    inspector = models.CharField(max_length=200, blank=False,
                                 verbose_name="指导教师")
    members = models.CharField(max_length=400, blank=False,
                               verbose_name="团队成员")
    im = models.CharField(max_length=50, blank=False, verbose_name="社交")
    year = models.CharField(max_length=10, blank=False, verbose_name="参加年份")

    class Meta:
        verbose_name = "参赛项目"
        verbose_name_plural = "参赛项目"

    def __unicode__(self):
        return self.title


class PreSubmit(models.Model):
    """
    inheribit table, which use ProjectSingle to show pre-submit content
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=str(uuid.uuid4()),
                                  verbose_name="初审报告唯一ID")
    project_id = models.OneToOneField(ProjectSingle)

    original = models.CharField(max_length=200, blank=True,
                                verbose_name="题目来源")
    background = models.TextField(blank=False, verbose_name="项目背景及研究意义")
    key_notes = models.TextField(blank=False,
                                 verbose_name="研究内容和拟解决的关键问题")
    innovation = models.TextField(blank=False, verbose_name="项目创新之处")
    progress_plan = models.TextField(blank=False, verbose_name="项目经费预算")
    pre_results = models.TextField(blank=False, verbose_name="预期研究成果")
    inspector_comments = models.TextField(blank=False,
                                          verbose_name="指导教师推荐语")
    school_comments = models.TextField(blank=False,
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
    project_id = models.OneToOneField(ProjectSingle)

    achievement_fashion = models.CharField(max_length=200, blank=True,
                                           verbose_name="成果形式")
    achievement_summary = models.TextField(blank=False,
                                           verbose_name="研究成果概述")
    inspector_comments = models.TextField(blank=False,
                                          verbose_name="指导教师推荐语")
    school_comments = models.TextField(blank=False,
                                       verbose_name="学校推荐语")

    class Meta:
        verbose_name = "项目结题报告"
        verbose_name_plural = "项目结题报告"

    def __unicode__(self):
        return self.project_id.title


class TechCompetition(models.Model):
    """
    Technology competition achievement, which follows FinalSubmit
    """
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=str(uuid.uuid4()),
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
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=str(uuid.uuid4()),
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
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=str(uuid.uuid4()),
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
    content_id = models.CharField(max_length=50,
                                  primary_key=True, default=str(uuid.uuid4()),
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
                               primary_key=True, default=str(uuid.uuid4()),
                               verbose_name="文件上传唯一ID")
    project_id = models.ForeignKey(ProjectSingle)
    name = models.CharField(max_length=100, blank=False,
                            verbose_name="文件名称")
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH + "/%Y/%m/%d")

    class Meta:
        verbose_name = "文件上传"
        verbose_name_plural = "文件上传"

    def __unicode__(self):
        return self.project_id.title

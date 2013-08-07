# coding: UTF-8

from django.db import models
from school.models import ProjectSingle
import datetime

class Student_Group(models.Model):
    email = models.EmailField(verbose_name=u"电子邮件")
    telephone = models.CharField(max_length=20, blank=True,
                                 verbose_name=u"联系电话")
    classInfo = models.CharField(blank=True, max_length=100,
                                 verbose_name=u"班级")
    studentId = models.CharField(blank=False, max_length=20,
                                 verbose_name=u"学号")
    studentName = models.CharField(blank=False, max_length=100,
                                   verbose_name=u"姓名")
    project = models.ForeignKey(ProjectSingle, blank=True)



    class Meta:
        verbose_name = "参赛学生信息"
        verbose_name_plural = "参赛学生信息"

    def __unicode__(self):
        return self.studentName

class StudentWeeklySummary(models.Model):
    project     = models.ForeignKey(ProjectSingle, verbose_name=u"项目")
    summary     = models.CharField(blank=True, max_length=500,
                               verbose_name=u"项目周报")
    date        = models.DateField(default=datetime.datetime.today)
    recorder    = models.CharField(blank=True, max_length=100,
                                verbose_name=u"记录人")
    weekId      = models.IntegerField(blank=False, verbose_name="周次", default=1)


class Funds_Group(models.Model):
    project_id = models.ForeignKey(ProjectSingle,blank = True)

    project_code = models.CharField(blank=False,max_length = 100,
                                 verbose_name = u"项目编号")
    
    funds_datetime = models.DateField(blank=False, max_length=100,
                                  verbose_name=u"报销日期")
    student_name = models.CharField(blank=False, max_length=100,
                                   verbose_name=u"报销人")
    funds_amount = models.CharField(blank=False, max_length=100,
                                 verbose_name=u"报销金额")
    funds_detail = models.CharField(blank=False, max_length=100,
                                 verbose_name=u"经费明细")
    funds_remaining = models.CharField(blank=False,max_length=100,
                                 verbose_name=u"经费余额")

    





   


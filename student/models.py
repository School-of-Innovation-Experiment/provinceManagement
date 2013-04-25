# coding: UTF-8
from django.db import models
from school.models import ProjectSingle

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

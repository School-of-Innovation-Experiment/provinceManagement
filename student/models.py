# coding: UTF-8
from django.db import models
from school.models import ProjectSingle

class Student_Group(models.Model):
    studentId = models.CharField(blank=False, max_length=20)
    studentName = models.CharField(blank=False, max_length=100)
    project = models.ForeignKey(ProjectSingle, blank=True)

    class Meta:
        verbose_name = "参赛学生信息"
        verbose_name_plural = "参赛学生信息"

    def __unicode__(self):
        return self.studentName

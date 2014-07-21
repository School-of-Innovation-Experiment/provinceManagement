# coding: UTF-8
from django.db import models
from school.models import *
import datetime

class TeacherMonthComment(models.Model):
    project = models.ForeignKey(ProjectSingle, verbose_name=u"项目")
    comment = models.CharField(blank=True, max_length=500,
                               verbose_name=u"项目月评")
    date = models.DateField(default=datetime.datetime.today)
    monthId  = models.IntegerField(blank=False, verbose_name="月次", default=0)
    class Meta:
        verbose_name = "教师项目月评"
        verbose_name_plural = "教师项目月评"

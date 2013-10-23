# coding: UTF-8

from django.contrib import admin
from student.models import *


RegisterClass = (Student_Group,
                 StudentWeeklySummary,
                 Funds_Group,
                )

for item in RegisterClass:
    admin.site.register(item)

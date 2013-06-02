# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: expert project relation
'''

import uuid

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User

from school.models import *
from users.models import *
from backend.logging import logger, loginfo
from const import FINANCIAL_CATE_A, FINANCIAL_CATE_B


exclude_schools_const = ("大连理工大学", "东北大学",
                         "大连民族学院", "大连海事大学",
                         "测试用学校",)

project_category_const = (FINANCIAL_CATE_A, FINANCIAL_CATE_B)


def save_record(expert, project):
    """
    """
    assigned_obj = Re_Project_Expert()
    assigned_obj.project = project
    assigned_obj.expert = expert
    assigned_obj.save()


def assigned_by_category(category, experts):
    """
    """
    projects = ProjectSingle.objects.filter(financial_category__category=category)

    loginfo(p=len(projects), label="Stage1:category")
    for school_str in exclude_schools_const:
        projects = projects.exclude(school__schoolName=school_str)

    loginfo(p=len(projects), label="Stage2:School exclude")

    project_count = len(projects)
    expert_count = len(experts)
    assigned_cnt = project_count / expert_count
    remaining_cnt = project_count - assigned_cnt * expert_count

    loginfo(p=expert_count, label="expert sum")

    j = 0
    expert = None
    for expert in experts:
        for i in range(0, assigned_cnt):
            save_record(expert, projects[i + j * assigned_cnt])
        j = j + 1
        loginfo(p="save record finish")

    for i in range(0, remaining_cnt):
        save_record(expert, projects[i + j * assigned_cnt])


def expert_assigned():
    """
    project assigned
    """
    experts = ExpertProfile.objects.filter()

    loginfo(p="A", label="Start")
    assigned_by_category(project_category_const[0], experts)

    loginfo(p="B", label="Start")
    assigned_by_category(project_category_const[1], experts)


def check():
    """
    """
    experts = ExpertProfile.objects.filter()
    loginfo(p=len(experts), label="Test, experts count")

    count = 0

    for expert in experts:
        assigned_projects = Re_Project_Expert.objects.filter(expert=expert)
        current_cnt = len(assigned_projects)
        count = count + current_cnt
        loginfo(p=current_cnt, label="Test, Experts Name")
        #check school
        for school_str in exclude_schools_const:
            check_projects = assigned_projects.filter(project__school__schoolName=school_str)
            loginfo(p=len(check_projects), label=school_str)

    loginfo(p=count, label="Test, Experts Name")


def delete_records():
    """
    """
    Re_Project_Expert.objects.filter().delete()

    loginfo(p="Delete all records!", label="Tools")

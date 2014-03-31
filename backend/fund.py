from adminStaff.models import ProjectPerLimits, ProjectControl, NoticeMessage, TemplateNoticeMessage
from adminStaff.forms import FundsChangeForm,StudentNameForm
from const import *
from student.models import  Student_Group, Funds_Group
from school.models import ProjectSingle, Project_Is_Assigned, Re_Project_Expert,UploadedFiles
from const.models import UserIdentity, InsituteCategory, ProjectGrade
from django.db import transaction
from django.db.models import Q
from backend.decorators import *
from backend.logging import loginfo

__metaclass__ = type
class CFundManage:
    @staticmethod
    def get_form_tabledata(project):
        project_funds_list = Funds_Group.objects.filter(project_id = project)
        fundsChange_group_form = FundsChangeForm();
        student_name_form = StudentNameForm(pid = project.project_id);
        ret = {
                "project_funds_list":project_funds_list,
                "fundsChange_group_form":fundsChange_group_form,
                "student_name_form":student_name_form,
                "project":project,
              }
        return ret

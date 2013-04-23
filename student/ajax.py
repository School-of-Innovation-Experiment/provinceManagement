# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from django.http import Http404
from django.utils import simplejson
from student.forms import StudentGroupForm
from student.models import Student_Group
from school.models import ProjectSingle

from const import MEMBER_NUM_LIMIT

@dajaxice_register
def MemberChange(request, form, form2):
    stugroup_form = StudentGroupForm(deserialize_form(form))
    if not stugroup_form.is_valid():
        ret = {'status': '2',
               'error_id': stugroup_form.errors.keys(),
               'message': u"输入有误，请重新输入"}
    elif not form2: # 添加或更新成员
        ret = new_or_update_member(request, stugroup_form)
    else:  # 更换成员
        ret = change_member(request, stugroup_form, StudentGroupForm(deserialize_form(form2)))
    return simplejson.dumps(ret)

def change_member(request, old_form, new_form):
    if not new_form.is_valid():
        ret = {'status': '2', "error_id": new_form.errors.keys(), 'message': u"输入有误，请重新输入"}
    else:
        ret = {'status': '0', 'message': u"人员变更成功"}
    return ret

def new_or_update_member(request, stugroup_form):
    student_id = stugroup_form.cleaned_data["student_id"]
    student_name = stugroup_form.cleaned_data["student_name"]
    try:
        project = ProjectSingle.objects.get(student__userid=request.user)
    except:
        raise Http404
    group = project.student_group_set
    for student in group.all():
        if student.studentId == student_id:
            student.studentName = student_name
            student.save()
            ret = {'status': '0', 'message': u"人员信息更新成功"}
            break
    else: # new student
        if group.count() == MEMBER_NUM_LIMIT[project.project_category.category]:
            ret = {'status': '1', 'message': u"人员已满，不可添加"}
        else:
            new_student = Student_Group(studentId = student_id,
                                        studentName = student_name)
            new_student.save()
            ret = {'status': '0', 'message': u"人员添加成功"}
    return ret

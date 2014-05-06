from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from school.models import ProjectSingle, PreSubmit, PreSubmitEnterprise, Teacher_Enterprise
from school.utility import create_newproject
from adminStaff.models import ProjectPerLimits
from const.models import ProjectOrigin, ProjectEnterpriseMaturity, ProjectEnterpriseOrigin, ProjectCategory, FinancialCategory
from const import FINANCIAL_CATE_UN, STUDENT_USER
from registration.models import RegistrationManager
from base64 import b64decode as b64de
from users.models import SchoolProfile, StudentProfile
from backend.logging import logger, loginfo

dispatcher = SimpleJSONRPCDispatcher(encoding=None)
Global_Request = None
ERROR_PROJ_EXIST = 1
ERROR_CANT_CREATE_USER = 2
ERROR_PROJ_SINGLE = 3
ERROR_PROJ_SUBMIT = 4
error_message = ['Success message',
                 'Project %s already exist!',
                 "Can't create user for Project %s",
                 'Some attribute error, please ensure all attributes of the project %s is filled!',
                 'Some error about the presubmit of project %s']

@csrf_exempt
def rpc_handler(request):
    global Global_Request
    Global_Request = request
    if len(request.POST):
        response = HttpResponse(mimetype="application/json")
        print request.raw_post_data
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
        response = HttpResponse()
        response.wirte("<b>Request ERROR: NO POST DATA</b><br>")

    response['Content-length'] = str(len(response.content))
    return response

def sync_proj(proj, user, schoolprofile):
    """
    Create ProjectSingle and Presubmit if it not exist in db
    """
    def create_proj_single(request, student_user):
        """
        create project single
        """
        newproj_single = ProjectSingle.objects.get(project_id=proj['project_id'])
        # newproj_single.adminuser = user
        # newproj_single.school = schoolprofile.school
        # student_profile = StudentProfile.objects.get(user = student_user)
        # newproj_single.student = student_profile

        proj_cate = ProjectCategory.objects.get(category=proj['project_category'])
        newproj_single.project_category = proj_cate
        financial_cate = FinancialCategory.objects.get(category=FINANCIAL_CATE_UN)
        newproj_single.financial_category = financial_cate
        for attr in projsingle_attrs:
            setattr(newproj_single, attr, proj[attr])
        newproj_single.save()
        return newproj_single

    def create_presubmit(proj_single):
        """
        create presubmit
        """
        newpresubmit = PreSubmit.objects.get(project_id=proj_single)
        # newpresubmit.project_id = proj_single

        origin = ProjectOrigin.objects.get(origin=proj['origin'])
        newpresubmit.content_id = newpresubmit.content_id
        newpresubmit.original = origin
        for attr in presubmit_attrs:
            setattr(newpresubmit, attr, proj[attr])
        newpresubmit.save()
        # return newpresubmit

    def create_presubmitenterprise(proj_single):
        """
        create presubmitenterprise
        """
        newpresubmitenterprise = PreSubmitEnterprise.objects.get(project_id=proj_single)
        # newpresubmitenterprise.project_id = proj_single
        origin = ProjectEnterpriseOrigin.objects.get(origin=proj['origin'])
        newpresubmitenterprise.original = origin
        maturity = ProjectEnterpriseMaturity.objects.get(maturity=proj['maturity'])
        # enterprise teacher
        enterprise_teacher = newpresubmitenterprise.enterpriseTeacher
        enterprise_teacher.name = proj['enterprise_teacher_name']
        enterprise_teacher.telephone = proj['enterprise_teacher_telephone']
        enterprise_teacher.titles = proj['enterprise_teacher_titles']
        enterprise_teacher.jobs = proj['enterprise_teacher_jobs']
        enterprise_teacher.save()
        # newpresubmitenterprise.enterpriseTeacher = enterprise_teacher
        # end
        for attr in presubmitenterprise_attrs:
            setattr(newpresubmitenterprise, attr, proj[attr])
        newpresubmitenterprise.save()
        # return newpresubmitenterprise

    if ProjectSingle.objects.filter(project_id=proj['project_id']).count():
        return ERROR_PROJ_EXIST, False
    projsingle_attrs = ['project_id', 'title', 'email', 'telephone', 'inspector',
                        'inspector_title', 'members', 'im', 'year', 'project_code']
    # fk: project_id, original, maturity, enterpriseTeacher
    presubmitenterprise_attrs = ['background', 'innovation', 'industry', 'product', 'funds_plan',
                                 'operating_mode', 'risk_management', 'financial_pred', 'inspector_comments',
                                 'school_comments']
    # fk: project_id, original
    presubmit_attrs = ['background', 'key_notes', 'innovation', 'progress_plan', 'funds_plan',
                       'pre_results', 'inspector_comments', 'school_comments']
    student_user = None
    try:
        global Global_Request
        request = Global_Request
        request.user = user
        student_user, _ = RegistrationManager().create_inactive_user(request, b64de(proj['student_username']),
                                                                     b64de(proj['student_person_firstname']),
                                                                     b64de(proj['student_password']),
                                                                     b64de(proj['student_email']),
                                                                     STUDENT_USER)
        result = create_newproject(request=request, new_user=student_user,
                                   financial_cate=FINANCIAL_CATE_UN,
                                   managername=b64de(proj['student_person_firstname']),
                                   pid=proj['project_id'])
    except Exception, err:
        if student_user:
            student_user.delete()
        logger.info(err)
        return ERROR_CANT_CREATE_USER, False
    try:
        proj_single = create_proj_single(request, student_user)
    except Exception, err:
        logger.info(err)
        return ERROR_PROJ_SINGLE, False
    try:
        if proj['presubmit_type'] == 'presubmit':
            create_presubmit(proj_single)
        else: create_presubmitenterprise(proj_single)
    except Exception, err:
        logger.info(err)
        # newpresubmitenterprise = PreSubmitEnterprise.objects.get(project_id=proj_single)
        # newpresubmitenterprise.enterpriseTeacher.delete()
        proj_single.student.user.delete()
        return ERROR_PROJ_SUBMIT, False
    return 0, True

def CheckSyncProjects(project_id):
    if ProjectSingle.objects.filter(project_id=project_id).count():
        return True
    else: return False

def SyncProjects(json_obj):
    """
    The main fuction for sync projects from school
    """
    def error_status(status, proj):
        """
        Return the error message according to the `status`
        """
        try:
            status = int(status)
            return error_message[status] % proj['title']
        except:
            return str(status)

    proj_singles = simplejson.loads(json_obj)
    username = b64de(proj_singles['username'])
    password = b64de(proj_singles['password'])
    user = authenticate(username=username, password=password)
    if user is None:
        return "Username or Password error!"
    try:
        schoolprofile = SchoolProfile.objects.get(userid=user)
    except:
        return "The account is not a school manager! %s %s" % (user.username, user.email)
    try:
        projlimits = ProjectPerLimits.objects.get(school=schoolprofile)
        projlimits_number = projlimits.number
    except:
        projlimits_number = 0
    if projlimits_number < len(proj_singles['projects']):
        return "Fail! You have only %s projects to Synchronization." % projlimits_number

    status, result, proj = -1, False, -1
    for proj in proj_singles['projects']:
        status, result = sync_proj(proj, user, schoolprofile)
        if not result:
            break
    else:
        return "%s Projects Synchronization Sucess!" % len(proj_singles['projects'])
    return error_status(status, proj)

def test(s):
    """
    test
    """
    return "Hello %s" % s

dispatcher.register_function(test, "test")
dispatcher.register_function(SyncProjects, "SyncProjects")
dispatcher.register_function(CheckSyncProjects, "CheckSyncProjects")

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from school.models import ProjectSingle, PreSubmit, PreSubmitEnterprise, Teacher_Enterprise
from adminStaff.models import ProjectPerLimits
from const.models import ProjectOrigin, ProjectEnterpriseMaturity, ProjectEnterpriseOrigin, ProjectCategory, FinancialCategory
from const import FINANCIAL_CATE_UN
from registration.models import RegistrationManager
from base64 import b64decode as b64de

dispatcher = SimpleJSONRPCDispatcher(encoding=None)
Global_Request = None
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
    def create_proj_single():
        """
        create project single
        """
        newproj_single = ProjectSingle()
        newproj_single.adminuser = user
        newproj_single.school = schoolprofile.school
        global Global_Request
        request = Global_Request
        request.user = user
        #TODO: new student_profile
        student_user, _ = RegistrationManager().create_inactive_user(request, b64de(proj['student_username']),
                                                                     b64de(proj['student_person_firstname']),
                                                                     b64de(proj['student_password']),
                                                                     b64de(proj['student_email']),
                                                                     STUDENT_USER)
        student_profile = StudentProfile.objects.get(user = student_user)
        newproj_single.student = student_profile
        proj_cate = ProjectCategory.objects.get(category=proj['project_category'])
        newproj_single.project_category = proj_cate
        financial_cate = FinancialCategory.objects.get(category=FINANCIAL_CATE_UN)
        newproj_single.financial_category = financial_cate
        for attr in projsingle_attrs:
            setattr(newproj_single, attr, proj[attr])
        return newproj_single

    def create_presubmit():
        """
        create presubmit
        """
        newpresubmit = PreSubmit()
        newpresubmit.project_id = proj_single
        origin = ProjectOrigin.objects.get(origin=proj['origin'])
        newpresubmit.original = origin
        for attr in presubmit_attrs:
            setattr(newpresubmit, attr, proj[attr])
        return newpresubmit

    def create_presubmitenterprise():
        """
        create presubmitenterprise
        """
        newpresubmitenterprise = PreSubmitEnterprise()
        newpresubmitenterprise.project_id = proj_single
        origin = ProjectEnterpriseOrigin.objects.get(origin=proj['origin'])
        newpresubmitenterprise.original = origin
        maturity = ProjectEnterpriseMaturity.objects.get(maturity=proj['maturity'])
        # enterprise teacher
        enterprise_teacher = Teacher_Enterprise()
        enterprise_teacher.name = proj['enterprise_teacher_name']
        enterprise_teacher.telephone = proj['enterprise_teacher_telephone']
        enterprise_teacher.titles = proj['enterprise_teacher_titles']
        enterprise_teacher.jobs = proj['enterprise_teacher_jobs']
        enterprise_teacher.save()
        newpresubmitenterprise.enterpriseTeacher = enterprise_teacher
        # end
        for attr in PreSubmitEnterprise_attrs:
            setattr(newpresubmitenterprise, attr, proj[attr])
        return newpresubmitenterprise

    if ProjectSingle.objects.get(project_id=proj['project_id']).count():
        return 1, False
    projsingle_attrs = ['project_id', 'title', 'project_category',
                        'email', 'telephone', 'inspector',
                        'inspector_title', 'members', 'im', 'year', 'project_code']
    # fk: project_id, original, maturity, enterpriseTeacher
    presubmitenterprise_attrs = ['content_id', 'background', 'innovation', 'industry', 'product', 'funds_plan',
                                 'operating_mode', 'risk_management', 'financial_pred', 'inspector_comments',
                                 'school_comments']
    # fk: project_id, original
    presubmit_attrs = ['content_id', 'background', 'key_notes', 'innovation', 'progress_plan', 'funds_plan',
                       'pre_results', 'inspector_comments', 'school_comments']
    try:
        proj_single = create_proj_single()
    except:
        return 2, False
    try:
        if proj['presubmit_type'] == 'presubmit':
            presubmit = create_presubmit()
        else: presubmit = create_presubmitenterprise()
    except:
        return 3, False
    proj_single.save()
    presubmit.save()
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
        error_message = ['Success message',
                         'Project %s already exist!',
                         'Some attribute error, please ensure all attributes of the project %s is filled!']
        return error_message[status] % proj['title']

    proj_singles = simplejson.loads(json_obj)
    username = b64de(proj_singles['username'])
    password = b64de(proj_singles['password'])
    user = authenticate(username=username, password=password)
    if user is None:
        return "Username or Password error!"
    try:
        schoolprofile = SchoolProfile.objects.get(userid=user)
    except:
        return "The account is not a school manager!"
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

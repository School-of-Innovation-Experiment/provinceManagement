from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from school.models import ProjectSingle, PreSubmit, PreSubmitEnterprise
from adminStaff.models import ProjectPerLimits
from const.models import ProjectOrigin
import base64

dispatcher = SimpleJSONRPCDispatcher(encoding=None)

@csrf_exempt
def rpc_handler(request):
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
    Create ProjectSingle if it not exist in db
    """
    def create_proj_single():
        newproj_single = ProjectSingle()
        newproj_single.adminuser = user
        newproj_single.school = schoolprofile.school
        #TODO: new student_profile
        #TODO: project category, [insitute]
        for attr in projsingle_attrs:
            setattr(newproj_single, attr, proj[attr])
        newproj_single.save()
        return newproj_single
    def create_presubmit():
        newpresubmit = PreSubmit()
        newpresubmit.project_id = proj_single
        origin = ProjectOrigin.objects.get(origin=proj['origin'])
        newpresubmit.original = origin
        for attr in presubmit_attrs:
            setattr(newpresubmit, attr, proj[attr])
        newpresubmit.save()

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
    if proj['presubmit_type'] == 'presubmit':
        create_presubmit()
    else: create_presubmitenterprise()
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
    username = base64.b64decode(proj_singles['username'])
    password = base64.b64decode(proj_singles['password'])
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

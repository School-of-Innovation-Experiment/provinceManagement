from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import simplejson
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
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

def sync_proj(poj):
    pass

def SyncProjects(json_obj):
    proj_singles = simplejson.loads(json_obj)
    username = base64.b64decode(proj_singles['username'])
    password = base64.b64decode(proj_singles['password'])
    user = authenticate(username=username, password=password)

    if user is None:
        return "Username or Password error!"
    return "login sucess! %s %s" % (username, password)
    for poj in proj_singles['pojects']:
        sync_proj(poj)

def test(s):
    """
    test
    """
    return "Hello %s" % s

dispatcher.register_function(test, "test")
dispatcher.register_function(SyncProjects, "SyncProjects")

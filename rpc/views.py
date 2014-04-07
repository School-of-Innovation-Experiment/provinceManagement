from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCDispatcher
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

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

def test(s):
    """
    test
    """
    return "Hello %s" % s

dispatcher.register_function(test, "test")

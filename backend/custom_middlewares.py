# coding: UTF-8
'''
Created on 2013-04-03

@author: tianwei

Desc: Custom Middleware 
'''

import os
import sys
import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from const import *
from const.models import * 
from adminStaff.models import *
from backend.logging import loginfo
from school.utility import get_current_year
from school.models import *



# Create your views here.
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from backend.decorators import *
from const import *

@csrf.csrf_protect
@login_required
# @authority_required(TEACHER_USER)
def home_view(request):
    return render(request, "teacher/teacher_home.html", {})

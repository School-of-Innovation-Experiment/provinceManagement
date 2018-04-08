# coding: UTF-8
'''
Created on 2013-04-02

@author: tianwei

Desc: Registration and login redirect
'''

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from backend.decorators import check_auth
from const import *


@login_required
def active(request, activation_key,
           template_name='registration/activate.html',
           extra_context=None):
    """
    Active the user account from an activation key.
    """
    from django.contrib.auth import logout
    identity = request.user.username[0]
    if identity in ('T', 'S', 'A'):
        # Logged in as a second-class user
        # Logout and Re-Login
        logout(request)
        return HttpResponseRedirect(request.path)
    if extra_context is None:
        extra_context = {}
    activation_key = activation_key.lower()
    profile = RegistrationProfile.objects.filter(activation_key=activation_key)
    if profile:
        target_username = profile[0].user.username
        username = request.user.username
        if target_username.endswith(username):
            # Activation key doesn't belong to this user
            account = RegistrationProfile.objects.activate_user(activation_key)
            return HttpResponseRedirect('/')
        message = u'激活链接不属于本帐户'
    else:
        # Invalid activation key
        message = u'激活链接无效!'
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(
        template_name,
        {'message': message},
        context_instance=context)


def register(request, success_url=None,
             form_class=RegistrationFormUniqueEmail, profile_callback=None,
             template_name='registration/registration_form.html',
             extra_context=None):
    """
     Allow a new user to register an account.
    """
    if request.method == "POST":
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(request, profile_callback=profile_callback)
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.
            return HttpResponseRedirect(success_url or reverse('registration_complete'))
    else:
        form = form_class()

    if extra_context is None:
        extra_context = {}

    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)

def login_redirect(request):
    """
    When the user login, it will decide to jump the according page, in other
    words, school user will be imported /school/ page, if the user have many
    authorities, the system will jump randomly
    """
    #TODO: I will use reverse function to redirect, like school and expert
    if check_auth(request.user, EXPERT_USER):
        return HttpResponseRedirect(reverse('expert.views.home_view'))
    elif check_auth(request.user, ADMINSTAFF_USER):
        return HttpResponseRedirect('/adminStaff/')
    else:
        return HttpResponseRedirect(reverse('switch'))


def login(request, template_name):
    if request.method == 'POST':
        username = request.POST.get('username')
        if not username or username != 'admin':
            raise Http404()
    from django.contrib.auth.views import login
    return login(request)


def logout(request, next_page):
    if not request.user.is_authenticated() or request.user.username != 'admin':
        raise Http404()
    from django.contrib.auth.views import logout
    return logout(request, next_page)

#!python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-05-12 18:03
# Last modified: 2017-05-12 18:23
# Filename: utils.py
# Description:
from random import choice

from django.conf import settings
from django.core.mail import send_mail as _send_mail

from backend.logging import loginfo


def send_mail(*args, **kwargs):
    auth_user, auth_password = choice(settings.EMAIL_POOL)
    loginfo(p='Send with ' + auth_user, label='send_mail')
    flag = _send_mail(auth_user=auth_user, auth_password=auth_password,
                      *args, **kwargs)
    return flag

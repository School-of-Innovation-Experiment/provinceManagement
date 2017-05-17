#!python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-05-12 18:03
# Last modified: 2017-05-17 18:40
# Filename: utils.py
# Description:
from random import choice

from django.conf import settings
from django.core.mail import send_mail as _send_mail

from backend.logging import loginfo, logger


def send_mail(subject, message, recipient_list, **kwargs):
    auth_user, auth_password = choice(settings.EMAIL_POOL)
    loginfo(p='Send with ' + auth_user, label='send_mail')
    try:
        flag = _send_mail(
                subject, message, auth_user, recipient_list,
                auth_user=auth_user, auth_password=auth_password,
                **kwargs)
    except Exception as e:
        logger.error(e)
        flag = False
    return flag

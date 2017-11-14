#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-12-01 15:42
# Last modified: 2017-06-01 16:12
# Filename: fab_update.py
# Description:
from fabric.api import cd, run, env, sudo


env.hosts = ['sie@192.168.20.100']
env.password = input('Server password:')
env.prompts = {"Type 'yes' to continue, or 'no' to cancel: ":'yes'}

def update():
    with cd('~/mysites/schoolManagement/deploy'):
        sudo('git checkout school')
        sudo('git pull origin school')
        sudo('python ../manage.py collectstatic')
        run('touch /tmp/uwsgi_reload')
        sudo('tail -n 50 ../../log/schoolManagement.log')

def restart():
    with cd('~/mysites/schoolManagement/deploy'):
        sudo('./restart_server.sh')
        sudo('/etc/init.d/nginx restart')
        run('ps aux|grep nginx|grep -v grep')
        run('ps aux|grep uwsgi|grep -v grep')


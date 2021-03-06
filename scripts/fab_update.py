# coding: UTF-8
from fabric.api import cd, run, env, sudo


env.hosts = ['sie@192.168.20.100']
env.password = raw_input('Server password:')
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


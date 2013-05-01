#!/bin/bash

#start scripts for provincemanagement
echo "************************************"
echo "welcome to use server deploy scripts"
echo "For Dalian university of technology"
echo "************************************"

if [ $1 = 'start' ];then
    echo "prepare for start uwsgi"
    psid=$(ps aux|grep "uwsgi"|grep -v "grep"|wc -l)
    echo "[debug]current process is":$psid
    if [ "$psid" -gt "2" ];then
        echo "uwsgi is running now!"
    else
        echo "execute uwsgi command..."
        sudo uwsgi --ini /etc/uwsgi/*.ini
    fi

    psid=$(ps aux|grep "nginx"|grep -v "grep"|wc -l)
    if [ "$psid" -gt "1" ];then
        echo "nginx is runnging now!"
    else
        echo "execute nginx command..."
        sudo /etc/init.d/nginx start
    fi

    echo "*_* Start uwsgi service[OK] *_* "
elif [ $1 = 'stop' ];then
    sudo killall -9 uwsgi
    sudo killall -9 nginx
    echo "*_* Stop uwsgi and nginx [OK] *_* "
elif [ $1 = 'restart' ];then
    sudo killall -9 uwsgi 
    sudo killall -9 nginx 
    sudo uwsgi --ini /etc/uwsgi/*.ini
    sudo /etc/init.d/nginx restart
    echo "*_* Restart uwsgi and nginx [OK] *_* "
elif [ $1 = 'deploy' ];then
    sudo cp school_server /etc/nginx/sites-available/
    sudo cp school_server.ini /etc/uwsgi/apps-available/
    sudo chmod 777 /var/run/nginx.pid
    echo "*_* Deploy and copy scipts *_*"
elif [ $1 = 'update' ];then
    echo "update production source code and update static files"
    cd $(cd "$(dirname "$0")"; pwd)/../
    echo "check branch to school"
    git checkout school
    echo "update code repo"
    git pull origin school
    git pull
    echo "update static folder"
    python manage.py collectstatic
    sudo chmod -R 777 ./*
    cd -
    echo "*_* update codebase *_*"
else
    echo "Usages: sh run.sh [start|restart|stop|deploy]"
fi

echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

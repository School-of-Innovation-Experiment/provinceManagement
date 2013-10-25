#!/bin/bash

loadini_func () {
    echo "load all ini files"
    dir="/etc/uwsgi/apps-available"
    filelist=`ls $dir/*.ini`
    for filename in $filelist;do
        echo $filename
        sudo uwsgi --ini $filename
    done
    echo "Finish the uwsgi operation!"
}

#start scripts for provincemanagement
echo "************************************"
echo "welcome to use server deploy scripts"
echo "For Dalian university of technology"
echo "************************************"

if [ $1 = 'start' ];then
    echo "prepare for start uwsgi"
    psid=$(ps aux|grep "uwsgi"|grep -v "grep"|wc -l)
    echo "[debug]ps":$psid
    if [ "$psid" -gt "2" ];then
        echo "uwsgi is running now!"
    else
        echo "execute uwsgi command..."
        loadini_func 
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
    echo "This command will shutdown all website in this server!!"
    sudo killall -9 uwsgi
    sudo killall -9 nginx
    echo "*_* Stop uwsgi and nginx [OK] *_* "

elif [ $1 = 'restart' ];then
    sudo killall -9 uwsgi 
    sudo killall -9 nginx 
    loadini_func 
    sudo /etc/init.d/nginx restart
    echo "*_* Restart uwsgi and nginx [OK] *_* "

elif [ $1 = 'deploy' ];then
    sudo cp school_server /etc/nginx/sites-available/school_server
    sudo ln -s /etc/nginx/sites-available/school_server /etc/nginx/sites-enabled/school_server
    sudo cp school_server.ini /etc/uwsgi/apps-available/
    sudo ln -s /etc/uwsgi/apps-available/school_server.ini /etc/uwsgi/apps-enabled/school_server.ini 
    sudo chmod 777 /var/run/nginx.pid
    echo "*_* Deploy and copy scipts *_*"

elif [ $1 = 'update' ];then
    echo "update production source code and update static files"
    cd $(cd "$(dirname "$0")"; pwd)/../
    echo "check branch to school"
    git checkout minzu 
    echo "update code repo"
    git pull origin minzu
    echo "update static folder"
    python manage.py collectstatic
    echo "*_* update codebase *_*"

else
    echo "Usages: sh run.sh [start|restart|stop|deploy]"
fi

echo "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

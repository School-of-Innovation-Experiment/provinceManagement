InnovationManagement
====================

A website for College students Innovation  Entrepreneurial  in Liaoning Province, it is Province Version 

# Environment 
 * Please, execute this cmd: **sudo pip install -r requirements.txt**

# How to install

 1. create database in mysql: create database ProvinceManagement character SET utf8;
 1. sync database in project root path: python manage.py syncdb
 1. migrate database: python manage.py migrate
 1. test server : python manage.py runserver IP:PORT
 1. visit your web browser: IP:PORT

# Q&A
 1. When you login the website, you may meet the follow issue:
   **Site matching query does not exist**
   Solve: 
    * python manage.py shell 
    * from django.contrib.sites.models import Site
    * new_site = Site.objects.create(domain='foo.com', name='foo.com')



#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-03-14 11:57
# Last modified: 2017-03-14 12:14
# Filename: update_id_from_backup.py
# Description:
import MySQLdb

con_local = MySQLdb.connect(host='localhost',user='root',passwd='root',
                            port=3306,db='DlutInnovationManagement')
cur_local = con_local.cursor()

con_remote = MySQLdb.connect(host='192.168.20.100',user='root',passwd='root',
                            port=3306,db='DlutInnovationManagement')
cur_remote = con_remote.cursor()

year = 2016

query = 'select project_id,project_unique_code from school_projectsingle '
query += 'where year={} and over_status_id=1;'

update_query = 'update school_projectsingle set project_unique_code="{}" '
update_query += 'where project_id="{}"'


cur_local.execute(query.format(year))
data = cur_local.fetchall()
for uid, iid in data:
    q = update_query.format(iid, uid)
    cur_remote.execute(q)

con_remote.commit()
con_remote.close()
con_local.close()

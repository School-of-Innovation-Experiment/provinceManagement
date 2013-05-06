#!/usr/bin/env python

# Work with cron:
#   $ chmod +x /path/to/this/script
#   $ crontab -e
#   $ 0 0 * * 0 /path/to/this/script # run this script every sunday(maybe)
#   $ service cron start  # or `/etc/init.d/cron start` or `start cron`
#   An alternative is to start the cron in bootup (e.g. add `/etc/init.d/cron start` to /etc/rc.local, using absolute path is IMPORTANT)
import sys
import os.path
import os
import logging
from datetime import datetime
from settings_production import DATABASES #DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD
DATABASE_NAME     = DATABASES["default"]["NAME"]
DATABASE_USER     = DATABASES["default"]["USER"]
DATABASE_PASSWORD = DATABASES["default"]["PASSWORD"]
# for remote dump
DATABASE_HOST     = DATABASES["default"]["HOST"]

BACKUP_DIR = "%s/db_backups" % os.path.dirname(os.path.abspath(__file__))
MYSQL_CMD = 'mysqldump'
ZIP_CMD = 'zip'

if not os.path.exists(BACKUP_DIR):
    os.mkdir(BACKUP_DIR)

def add_time_to_debug(function):
    now_time = lambda: datetime.now().strftime("Record at %y-%m-%d, %H:%M:%S :")
    def _timed_func(*args, **kwargs):
        '''
        the first item of args is a string
        '''
        function(now_time()+args[0], *args[1:], **kwargs)
    return _timed_func

logging.basicConfig(level=logging.DEBUG,
                    # if do only record to stdout, using stream,
                    # otherwise, using filename
                    # stream=sys.stdout,
                    filename=os.path.join(BACKUP_DIR, "db_backup.log"))
# record time for every logging.debug
logging.debug = add_time_to_debug(logging.debug)

def _setup():
    if not os.path.exists(BACKUP_DIR):
        logging.debug("Created backup directory %s" % BACKUP_DIR)
        os.mkdir(BACKUP_DIR)
    else:
        logging.debug("Using backup directory %s" % BACKUP_DIR)

def _backup_name():
    now = datetime.now()
    time_name = now.strftime("%y-%m-%d_%H-%M-%S")
    file_name = "_%s.sql" % time_name.lower()
    logging.debug("Setting backup name at %s as %s" % (time_name, file_name))

    return file_name

def _run_backup(file_name):
    host_cmd = ("-h %s" % DATABASE_HOST) if DATABASE_HOST else ""
    cmd = "%(mysqldump)s %(host)s -u %(user)s --password=%(password)s %(database)s > %(log_dir)s/%(file)s" % {
        'mysqldump' : MYSQL_CMD,
        'user' : DATABASE_USER,
        'password' : DATABASE_PASSWORD,
        'database' : DATABASE_NAME,
        'log_dir' : BACKUP_DIR,
        'file': file_name,
        'host': host_cmd}
    logging.debug("Backing up with command %s " % cmd)
    return os.system(cmd)

def _zip_backup(file_name):
    backup = "%s/%s" % (BACKUP_DIR, file_name)
    zipfile_name = "%s.zip" % (backup)

    if os.path.exists(zipfile_name):
        logging.debug("Removing previous zip archive %s" % zipfile_name)
        os.remove(zipfile_name)
    zip_cmds = {'zip' : ZIP_CMD, 'zipfile' : zipfile_name, 'file' : backup }

    # Create the backup
    logging.debug("Making backup as %s " % zipfile_name)
    os.system("%(zip)s -q -9 %(zipfile)s %(file)s" % zip_cmds)

    # Test our archive
    logging.debug("Testing zip archive")
    if not os.system("%(zip)s -T -D -q %(zipfile)s" % zip_cmds):
        # If there was no problem, then delete the unzipped version
        os.remove(backup)
        return True
    else:
        return False

def main(*args):
    _setup()
    file_name = _backup_name()
    _run_backup(file_name)
    return True
    # need `zip` depandence
    # return(_zip_backup(file_name))

if __name__ == '__main__':
    sys.exit(main(*sys.argv))

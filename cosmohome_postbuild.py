#!/usr/bin/env python

import os
from os import system as sh
import os.path as osp
import sys
from time import sleep
import _mysql_exceptions

sys.path.append('/root/boinc/py')
import boinc_path_config
from Boinc import database, configxml



print "Copying project files to data volume..."
sh('cp -r /root/projects.build/cosmohome /root/projects')
for x in ['html', 'html/cache', 'upload', 'log_cosmohome']: 
    sh('chmod -R g+w /root/projects/cosmohome/'+x)


if not '--copy-only' in sys.argv:
    
    print "Creating database..."
    while True:
        try:
            database.create_database(
                srcdir = '/root/boinc',
                config = configxml.ConfigFile(filename='/root/projects/cosmohome/config.xml').read().config,
                drop_first = False
            )
        except _mysql_exceptions.ProgrammingError as e:
            if e[0]==1007: 
                print "Database exists, not overwriting."
                break
            else:
                raise
        except _mysql_exceptions.OperationalError as e:
            if e[0]==2003:  
                print "Waiting for mysql server..."
                sleep(1)
            else: 
                raise
        else:
            sh('cd /root/projects/cosmohome/html/ops; ./db_schemaversion.php > /root/projects/cosmohome/db_revision')
            break


    print "Running BOINC update scripts..."
    os.chdir('/root/projects/cosmohome')
    sh('bin/xadd')
    sh('(%s) | bin/update_versions'%('; '.join(['echo y']*10)))

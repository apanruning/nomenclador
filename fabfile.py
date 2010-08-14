#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$
"""Deployment script.

This script is coded so it can make the deployments automagically in the 
designed servers, it also works as a documentation of where are the programs 
installed.

USE: fab <hosts>:<username> <action>
EX: fab staging:admin release
"""

__author__ = "$Author$"
__version__ = "$Revision$"
__date__ = "$Date$"

import os
import sys
import tempfile
import datetime
from string import Template
from fabric.api import env, run, local, require, put, sudo, prompt, cd

BASE_DIR = os.path.dirname(__file__)
env.project_name = BASE_DIR.split('/')[-1:].pop()

WSGI_TEMPLATE = Template('''
import sys, os, site

site.addsitedir('$virtual_env/lib/python2.6/site-packages/')

# Add a custom Python path.
sys.path.append('$deploy_dir')
sys.path.insert(0,'$deploy_dir/apps')

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "production"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
    ''')
    
APACHE_TEMPLATE = Template('''
<VirtualHost *:80>
    ServerAdmin maturburu@gmail.com
    ServerName $project_name.com
    ServerAlias *.$project_name.com
    DocumentRoot $deploy_dir
    ErrorLog /var/log/apache2/error.$project_name.log
    WSGIDaemonProcess $project_name processes=2 maximum-requests=500 threads=15
    WSGIProcessGroup $project_name
    WSGIScriptAlias / $virtual_env/bin/$project_name.wsgi
    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn
    CustomLog /var/log/apache2/access.$project_name.log combined
</VirtualHost>
    ''')

env.deploy_dir = '/opt/sites/%s' %env.project_name
env.virtual_env = '/opt/venvs/%s' %env.project_name
env.apache_command = 'apache2ctl restart'

def development():
    env.hosts = ["localhost"]

def staging(username="mherrero", hosts=["mherrero.webfactional.com"]):
    env.user = username
    env.hosts = hosts
    env.deploy_dir = '/home/mherrero/webapps/cyj/nomenclador'
    env.virtual_env = '/home/mherrero/webapps/cyj/venv'
    env.apache_command = '/home/mherrero/webapps/cyj/apache2/bin/restart'

def production(username="root", hosts=["nomenclador.comercioyjusticia.com.ar"]):
    env.user = username
    env.hosts = hosts
    
def write_template(file_name, template):
    rendered_file = open(file_name, 'w')
    rendered_file.write(template.safe_substitute(env))
    rendered_file.close()

    return rendered_file

def wsgi_config():
    file_name = '%s.wsgi'%env.project_name
    wsgi_file = write_template(file_name, WSGI_TEMPLATE)
    
def apache_config():
    file_name = '%s.conf'%env.project_name
    apache_file = write_template(file_name, APACHE_TEMPLATE)

def release():
    """Creates a tarball, uploads it and decompresses it in the rigth path."""
    require("hosts", provided_by=[development, staging, production])
    
    tmpdir = tempfile.mkdtemp()
    tar = "%s-%s.tar.bz2" % (env.project_name ,datetime.datetime.now().strftime("%Y%m%d%H%M%S"),)
    local("git archive | gzip > %s" %tar)
    local("cd %s/%s; /bin/tar cfj %s/%s *" % (tmpdir, env.project_name, tmpdir, tar,))
    put("%s/%s" % (tmpdir, tar), tar)
    # warning: contents in destination directory will be lost.
    run("tar xfj %s -C %s" % (tar, env.deploy_dir))
    run("rm -rf %s %s" % (tmpdir, tar))
    local("rm -rf %s %s" % (tmpdir, tar))

def apache_restart():
    """Restarts the program in the servers."""
    require("hosts", provided_by=[development, staging, production])
    run(env.apache_command)

# vim: set fenc=utf-8 tw=79 sw=4 ts=4 sts=4 ai et:

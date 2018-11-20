# -*- coding: utf-8 -*-

from fabric import Connection
from invoke import task


SITE_DIR = '~/sites/flask-api-users'
VENV = '~/venvs/'
PYTHON_BIN = VENV + 'bin/python'
PIP_BIN = VENV + 'bin/pip'


def whoami(c):
    """
    Print the envirioment and user
    """
    c.run('whoami')


def git(conn, cmd):
    """
    Create a method to execute git on the server
    """
    with conn.cd('{}'.format(SITE_DIR)):
        conn.run('git {}'.format(cmd))


def checkout(conn, branch='master', tag=None):
    """
    Run git checkout to branch or tag
    """
    if tag:
        git(conn, 'checkout {}'.format(tag))

    else:
        git(conn, 'checkout {}'.format(branch))


def pull(conn):
    """
    Run git pull command on repository
    """
    git(conn, "pull")


def fetch(conn):
    """
    Run git pull command on repository
    """
    git(conn, "fetch")


def sudo(conn, cmd):
    conn.sudo(cmd)


def install_requirements(conn, env='prod'):
    """
    Install all requirements by the server
    """
    cmd = "{} install -r requirements/{}.txt".format(PIP_BIN, env)
    with conn.cd('{}'.format(SITE_DIR)):
        conn.run(cmd)


@task
def uname(c):
    """ Prints information about the host. """
    c.run('uname -a')
    whoami(c)


def restart(conn):
    """
    Restart supervisor and webserver
    """
    conn.sudo("supervisorctl restart api_users:gunicorn_api_users")
    conn.sudo("service nginx restart")


@task
def status(c):
    """
    Status supervisor and webserver
    """
    c.sudo("supervisorctl status api_users:gunicorn_api_users")
    c.sudo("service nginx status")


@task
def stop(c):
    """
    Stopping supervisor
    """
    c.sudo("supervisorctl stop api_users:gunicorn_api_users")


@task
def deploy(c, tag=None):
    """
    Deploy the code to context
    """

    fetch(c)

    if tag:
        checkout(c, tag)
    else:
        checkout(c)

    install_requirements(c)

    restart(c)


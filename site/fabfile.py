import os
from fabric.api import local, lcd, prefix


SITE_NAME = 'djagon'
SITE_ROOT = os.path.dirname(__file__)
SOURCE_ROOT = os.path.join(SITE_ROOT, 'source')
SETTINGS_ROOT = os.path.join(SITE_ROOT, 'conf/settings')
ACTIVATE_VIRTUALENV = '. {}'.format(os.path.join(SITE_ROOT, 'var/virtualenv/%s/bin/activate' % SITE_NAME))
SUPERVISOR_CONFIG = os.path.join(SITE_ROOT, 'conf/supervisor/supervisord.conf')


__all__ = ['deploy', 'restart']


def deploy():
    """
    Deploy/re-deploy the project
    """
    with lcd(SITE_ROOT):
        local('git pull')
        with prefix(ACTIVATE_VIRTUALENV):
            local('pip install -r requirements.pip')
            local('python manage.py syncdb --migrate')
            local('python manage.py collectstatic --noinput')
    restart()


def restart(app='all'):
    """
    Restart Gunicorn processes using Supervisor

    You may restart separate process:

        fab restart:site
        fab restart:game

    Or you may restart all of them:

        fab restart
    """
    with lcd(SITE_ROOT):
        with prefix(ACTIVATE_VIRTUALENV):
            local('supervisorctl -c %s restart %s' % (SUPERVISOR_CONFIG, app))

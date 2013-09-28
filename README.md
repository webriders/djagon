Djagon
======
This is DjangoDash 2013 contest project (why "Djagon"? Let's say that it means something :)

The idea of this project is to implement online multiplayer "Uno" card game.
And at the first place - to make it fun and entertaining!

![UNO header](http://i.imgur.com/UHQD55q.jpg)

We are doing this just for fun, without any selfish purposes nor for profit.
All rights for the Uno card game belongs to [Mattel](http://en.wikipedia.org/wiki/Mattel).

Requisites
----------
You need to have Python (and python-dev), pip, virtualenv and [libevent](http://www.libevent.org/) installed on your system.

python.dev installation tips:
- Debian/Ubuntu: `sudo apt-get install python-dev`

libevent installation tips:
- Debian/Ubuntu: `sudo apt-get install libevent-dev`
- Mac OS X: `brew install libevent`

Install
-------

First of all, go to your workspace dir and clone the Git repo:

    git clone https://github.com/webriders/djagon

Notice: all further commands should be executed within djagon/site/ directory:

    cd djagon/site/

### Easy way

Use Fabric (we assume that you have already installed it):

    fab install

### Advanced way

Don't worry, it's still quite easy.

1. Create, activate and setup virtualenv:
        virtualenv var/virtualenv/djagon
        source var/virtualenv/djagon/bin/activate
        pip install -r requirements.pip

If something went wrong with pip install - probably it's Gevent, [read more](http://www.gevent.org/) about it's installation.

2. Setup project:
        cp conf/settings/local.py.dev-sample conf/settings/local.py  # this is an example settings file
        nano conf/settings/local.py # setup there private settings (DB, secret keys, etc.)
                                    # there is a setting: GAME_SOCKET_URL - this is URL where you run
                                    # gunicorn + gevent + socketio server, read below
        ./manage.py syncdb --migrate

Run
---
You need to setup & run 2 servers: one for Django site, second for WebSockets

Next example is for development / quick start:

    ./manage.py runserver &
    gunicorn --worker-class=socketio.sgunicorn.GeventSocketIOWorker --bind=0.0.0.0:9000 --debug conf.wsgi:application &

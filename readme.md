# [SpaceShare](https://spaceshare.me)   [![Build Status](https://travis-ci.org/DavidAwad/SpaceShare.svg?branch=master)](https://travis-ci.org/DavidAwad/SpaceShare) [![Coverage Status](https://coveralls.io/repos/DavidAwad/SpaceShare/badge.svg)](https://coveralls.io/r/DavidAwad/SpaceShare) [![Code Climate](https://d3s6mut3hikguw.cloudfront.net/github/DavidAwad/SpaceShare/badges/gpa.svg)](https://d3s6mut3hikguw.cloudfront.net/github/DavidAwad/SpaceShare/) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/DavidAwad/SpaceShare?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=body_badge)

# "Share your thing like it ain't no thang"

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/DavidAwad/SpaceShare)

[![Deploy to Bluemix](https://bluemix.net/deploy/button.png)](https://bluemix.net/deploy?repository=https://github.com/davidawad/SpaceShare)


## REST API Coming Soon!
## Being rebuilt using react and celery

### This is a File sharing platform  meant to simplify file sharing between persons and groups of people by removing the need to login. It is not secure, it's not meant to be, it's meant to be the extreme trade off between convenience and security.

#### "Sometimes you just need to move something, and you just don't care if someone else finds it."

#### You go to spaceshare.me, upload your file, attach a number.
#### Others can go to the site and give that integer; or go to [spaceshare.me/upload/number](spaceshare.me/upload/number) and it will give you the file.

#### Built using Flask, and Celery with Redis as a task broker and using a gridFS mongodb to store uploaded files. The frontend is using foundation but will eventually switch to react and twitter bootstrap

I want this to be a really accessible project to newbies and pros alike so I will be writing a lot of documentation in the near future.

## Requirements
- Python Flask
- MongoDB
- Redis
- Celery
- React
- Gulp
- bower
- npm


## Running the project for Development

1. run the Flask Server
```
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

git clone https://github.com/DavidAwad/SpaceShare/

cd SpaceShare

make run

gulp

celery worker -A tasks --loglevel=info

redis-server

./mongod (however you run mongo on your machine)

```
If you get an error it's possible you're simply not running MongoDB, SpaceShare checks on the default port for a mongo connection.

2. Download the monngodb [binaries](https://www.mongodb.org/downloads) for your machine.
You'll want to go into the /bin subfolder where you'll find a bunch of mongo named executabled.
One of them will be named *mongod*, this is the mongodb server executable. This is what makes mongo work.
What you want to do here is tell mongodb where you're going to store your data.

`./mongod --config mongodb.config`

3. Access app from localhost:5000 (wherever your terminal says it is)



## Getting Started
So SpaceShare has a lot going on that may not necessarily make sense to a python beginner or someone new to coding in general(which I always try to make my repo's because I would have ). I have begun slowly writing the mass of documentation that needs to be written for everything that's going on here.

<br>

|    Files    | What is it?           |
| :-------------: |:-------------:|
| [.travis.yml](https://github.com/DavidAwad/SpaceShare/wiki/Travis-CI)   | So I use travis CI for my integration testing to make sure things aren't broken. I will soon write a good chunk about it in the wiki. |
| [Procfile](https://devcenter.heroku.com/articles/procfile)      | The Procfile is essentially the file that Heroku uses to run a specific command to run your python server. More documentation to come at that link.      |
| [.gitignore](https://help.github.com/articles/ignoring-files/) | The gitignore is essentially a list of files I have on my own local machine that are either personal or I don't want to leave in the git repo, that's why it has seemingly random things in it.      |
|[robots.txt](http://camosunweb.com/robots-txt/) and [humans.txt](http://humanstxt.org)  | The robots file contains information for web crawlers that search your web pages, while humans.txt is a bit more fun, check out the link for that. |

## Possible Errors you might get
#### If you're on OSX you might find that the virtualenv needs python 2.7.9 and not 2.7.6 because of the built in python version. This is something that can be really frustrating if you don't have some good shell knowledge.
```shell
virtualenv venv -p /usr/local/bin/python
```

## can't import celery?

```Python
(venv)➜  spaceshare git:(master) ✗ make run
python spaceshare/__init__.py
INFO:werkzeug: * Running on http://127.0.0.1:4000/ (Press CTRL+C to quit)
INFO:werkzeug: * Restarting with stat
INFO:werkzeug: * Detected change in '/Users/david/Code/spaceshare/spaceshare/__init__.py', reloading
INFO:werkzeug: * Restarting with stat
Traceback (most recent call last):
  File "spaceshare/__init__.py", line 3, in <module>
    from tasks import print_words
  File "/Users/david/Code/spaceshare/spaceshare/tasks.py", line 3, in <module>
    from celery import Celery
  File "/Users/david/Code/spaceshare/venv/lib/python2.7/site-packages/celery/__init__.py", line 130, in <module>
    from celery import five
  File "/Users/david/Code/spaceshare/venv/lib/python2.7/site-packages/celery/five.py", line 51, in <module>
    from kombu.five import monotonic
  File "/Users/david/Code/spaceshare/venv/lib/python2.7/site-packages/kombu/five.py", line 52, in <module>
    libSystem = ctypes.CDLL('libSystem.dylib')
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/ctypes/__init__.py", line 365, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: dlopen(libSystem.dylib, 6): image not found
make: *** [run] Error 1
(venv)➜  spaceshare git:(master) ✗ unset DYLD_FALLBACK_LIBRARY_PAT
```

## Useful Flask Resources to Learn what's happening :
### [File Input in Flask](http://runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python) by [Michael Molina](http://runnable.com/u/mmolina)
### [Simple Flask Guest Book](https://github.com/x/Simple-Flask-Guest-Book) by [Devin Peticolas](https://github.com/x)
### [Flask Talk f2014](https://github.com/usacs/flaskTalkF2014) by [Vaibhav Vverma](https://github.com/v)
### [Flask Database Talk](https://github.com/kaushal/databaseTalk2014) by [Kaushal Parikh](https://github.com/kaushal)


## Special Thanks :
### [Joel Pena](https://github.com/jpena29), [Devon Peticolas](https://github.com/x), and [Wisdom Omuya](https://github.com/deafgoat) from MongoDB, and of course StackOverflow made this app Possible. Thank you sincerely.

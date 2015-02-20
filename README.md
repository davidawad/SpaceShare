# [SpaceShare](https://spaceshare.me)   [![Build Status](https://travis-ci.org/DavidAwad/SpaceShare.svg?branch=master)](https://travis-ci.org/DavidAwad/SpaceShare) [![Coverage Status](https://coveralls.io/repos/DavidAwad/SpaceShare/badge.svg)](https://coveralls.io/r/DavidAwad/SpaceShare)

# "Share your thing like it ain't no thang"

## REST API Coming Soon!

### This is a File sharing platform  meant to simplify file sharing between persons and groups of people by removing the need to login.

#### "Sometimes you just need to move something, and you just don't care if someone else finds it."

#### You go to spaceshare.me, upload your file, give it a number.
#### Others can go to the site and give that integer; or go to [spaceshare.me/upload/number](spaceshare.me/upload/number) and it will give you the file.

#### Built using Flask, using mongodb with gridFS to store uploaded files.
I want this to be a really accessible project to newbies and pros alike so I will be writing a lot of documentation in the near future. As of right now classes are starting up and getting slightly crazy but I'm finding the time.

## Dependencies

### In your terminal,
```bash
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Run the server

1. run the Flask Server
```
cd [REPO LOCATION]
python __init__.py
```
2. Download the monngodb [binaries](https://www.mongodb.org/downloads) for your machine.
You'll want to go into the /bin subfolder where you'll find a bunch of mongo named executabled.
One of them will be named *mongod*, this is the mongodb server executable. This is what makes mongo work.
What you want to do here is tell mongodb where you're going to store your data.

`./mongod --config mongodb.config`

3. Access app from localhost:5000 (wherever your terminal says it is)

So SpaceShare has a lot going on that may not necessarily make sense to a python beginner or someone new to coding in general(which I always try to make my repo's because I would have ). I have begun slowly writing the mass of documentation that needs to be written for everything that's going on here.

<br>

[.travis.yml](https://github.com/DavidAwad/SpaceShare/wiki/Travis-CI) So I use travis CI for my integration testing to make sure things aren't broken. I will soon write a good chunk about it in the wiki.

[Procfile](https://devcenter.heroku.com/articles/procfile) The Procfile is essentially the file that Heroku uses to run a specific command to run your python server. More documentation to come at that link.

[.gitignore](https://help.github.com/articles/ignoring-files/)
	 	The gitignore is essentially a list of files I have on my own local machine that are either personal or I don't want to leave in the git repo, that's why it has seemingly random things in it.

[robots.txt](http://camosunweb.com/robots-txt/) and [humans.txt](http://humanstxt.org)
		The robots file contains information for web crawlers that search your web pages, while humans.txt is a bit more fun, check out the link for that.

## Useful Flask Resources to Learn what's happening :
### [File Input in Flask](http://runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python) by [Michael Molina](http://runnable.com/u/mmolina)
### [Simple Flask Guest Book](https://github.com/x/Simple-Flask-Guest-Book) by [Devin Peticolas](https://github.com/x)
### [Flask Talk f2014](https://github.com/usacs/flaskTalkF2014) by [Vaibhav Vverma](https://github.com/v)
### [Flask Database Talk](https://github.com/kaushal/databaseTalk2014) by [Kaushal Parikh](https://github.com/kaushal)


## Special Thanks :
### [Joel Pena](https://github.com/jpena29), [Devon Peticolas](https://github.com/x), and [Wisdom Omuya](https://github.com/deafgoat) from MongoDB, and of course StackOverflow made this app Possible. Thank you sincerely.

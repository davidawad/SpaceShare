The way Spaceshare works, is that it uses the MVC model, with React manipulating a modular, modern frontend, Flask acting as middleware and with celery tasks doing most of the work behind the scenes.

It uses Bower for frontend dependency management and Gulp as a task runner.


### Show me the code.

The React tags all live in `static/jsx/app.jsx`.

The celery tasks live inside of `spaceshare/tasks.py`. This is where the saving files should be happening.

The app middleware, controllers and routing logic is currently inside of `spaceshare/__init__.py`, which it shouldn't be, and they will soon be moved to `routing.py` and this will be updated when that changes.


## Running the project for Development

run the Flask Server
```
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

git clone https://github.com/DavidAwad/SpaceShare/

cd SpaceShare

make run

gulp

cd spaceshare

celery worker -A tasks --loglevel=info

redis-server

./mongod (or however you run mongo on your machine)
```
If you get an error it's possible you're simply not running MongoDB, SpaceShare checks on the default port for a mongo connection.


### Download mongodb [binaries](https://www.mongodb.org/downloads) for your machine.
You'll want to go into the /bin subfolder where you'll find a bunch of mongo named executabled.
One of them will be named *mongod*, this is the mongodb server executable. This is what makes mongo work.
What you want to do here is tell mongodb where you're going to store your data.

`./mongod --config mongodb.config`

Access spaceshare on [http://localhost:4000](http://localhost:4000)


#### whoa, what are all these random files?

|    File    | What is it?           |
| :-------------: |:-------------:|
|[.bowerrc](http://bower.io)|This file specifies the directory that bower will store it's frontend dependencies|
|[.coveralls.yml](http://coveralls.io)|This file specifies the api key for coveralls which does static code analysis on repositories to improve code quality |
|[.gitignore](https://help.github.com/articles/ignoring-files/)|The gitignore is essentially a list of files I have on my own local machine that are either personal or I don't want to leave in the git repo, that's why it has seemingly random things in it|
|[.travis.yml](https://github.com/DavidAwad/SpaceShare/wiki/Travis-CI)|So I use travis CI for my integration testing to make sure things aren't broken. I will soon write a good chunk about it in the wiki. |
|[bower.json](http://bower.io)|This file specifies the dependencies that bower is managing for us|
|[gulpfile.js](http://gulpjs.com)|This file specifies the tasks that we want gulp to perform for us. Like watchng our react JSX in order to compile it whenever we make a change|
|[Makefile](https://www.gnu.org/software/make/)|This file specifies the tasks that we want gulp to perform for us. Like watching our react JSX in order to compile it whenever we make a change|
|[package.json](https://docs.npmjs.com/files/package.json)|This is a file generated my npm that specifies which javascript tools to keep track of in your project|
|[Procfile](https://devcenter.heroku.com/articles/procfile)|The Procfile is essentially the file that Heroku uses to run a specific command to run your python server. More documentation to come at that link|
|[requirements.txt](http://pip.readthedocs.org/en/stable/quickstart/)|Most Python projects use a module dependency manager called pip. This file specifies what modules that your python project is using for pip|






## Useful Flask Resources to Learn what's being put together :
### [Getting used to Flask, React and Gulp](https://realpython.com/blog/python/the-ultimate-flask-front-end/)
### [File Input in Flask](http://runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python) by [Michael Molina](http://runnable.com/u/mmolina)
### [Simple Flask Guest Book](https://github.com/x/Simple-Flask-Guest-Book) by [Devin Peticolas](https://github.com/x)
### [Flask Talk f2014](https://github.com/usacs/flaskTalkF2014) by [Vaibhav Vverma](https://github.com/v)
### [Flask Database Talk](https://github.com/kaushal/databaseTalk2014) by [Kaushal Parikh](https://github.com/kaushal)

# [SpaceShare](spaceshare.me)

##NOT WORKING JUST YET


### This is a File sharing platform  meant to simplify file sharing between groups of people. 
### You go to spaceshare.me, upload your file, give it a **number**. 
### Others go to spaceshare.me/uploads/**number** and it will give you the file. 

####Built using Flask, Deployed on digitalocean using mongodb with gridFS to store the files that are uploaded.



##To Run This on your local Host

## Get your PIP (Python dependency manager)

### If you have a mac

_if you have easy_install already, just skip to step 3, you can test by typing ```which easy_install``` in your terminal_

1. Download the distribute setup script to get easy_install
```
http://python-distribute.org/distribute_setup.py
```

2. Run the script to install easy_install (do this in the terminal)
```
python distribute_setup.py
```

3. easy_install pip (do this in the terminal)
```
easy_install pip
```

### If you're on Windows

1. Install pip-Win
```
https://sites.google.com/site/pydatalog/python/pip-for-windows
```

### If you're on Ubuntu

1. Install with Apt (in terminal)
```
sudo apt-get install python-pip
```

## Install Dependencies

1. In your terminal, 
```
pip install flask
pip install pymongo
pip install gridfs
```

## Run the server

1. In your terminal, navigate to the repo's directory and run __init__.py
```
cd [REPO LOCATION]
python __init__.py
```

2. Access app from localhost:5000


## Other Useful Flask Examples To Learn what's happening :
##[Simple Flask Guest Book](https://github.com/x/Simple-Flask-Guest-Book) by [Devin Peticolas](https://github.com/x)
##[Flask Talk f2014](https://github.com/usacs/flaskTalkF2014) by [Vaibhav Vverma](https://github.com/v)
##[Flask Database Talk](https://github.com/kaushal/databaseTalk2014)   

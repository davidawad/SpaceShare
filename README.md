# [SpaceShare](https://spaceshare.me)   [![Build Status](https://travis-ci.org/DavidAwad/SpaceShare.svg?branch=master)](https://travis-ci.org/DavidAwad/SpaceShare)


#Share your thing like it ain't no thang.

### This is a File sharing platform  meant to simplify file sharing between persons and groups of people by removing the need to login.

####"Sometimes you just need to move something, and you just don't care if someone else finds it." 

#### You go to spaceshare.me, upload your file, give it a number. 
#### Others go to [spaceshare.me/upload/number](spaceshare.me/upload/number) and it will give you the file. 

####Built using Flask, using mongodb with gridFS to store uploaded files.

##Dependencies 

1. In your terminal, 
```bash
pip install -r requirements.txt
```

## Run the server

1. run the Flask Server
```
cd [REPO LOCATION]
python __init__.py
```
2. Download the monngodb [binaries](https://www.mongodb.org/downloads) for your machine. 

`./mongod --config mongodb.config`

3. Access app from localhost:5000 (wherever your terminal says it is)


## Useful Flask Resources to Learn what's happening :
##[File Input in Flask](http://runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python) by [Michael Molina](http://runnable.com/u/mmolina)
##[Simple Flask Guest Book](https://github.com/x/Simple-Flask-Guest-Book) by [Devin Peticolas](https://github.com/x)
##[Flask Talk f2014](https://github.com/usacs/flaskTalkF2014) by [Vaibhav Vverma](https://github.com/v)
##[Flask Database Talk](https://github.com/kaushal/databaseTalk2014) by [Kaushal Parikh]()

## Special Thanks
### [Joel Pena](https://github.com/jpena29), [Devon Peticolas](https://github.com/x), and [Wisdom Omuya](https://github.com/deafgoat) from MongoDB, and of course StackOverflow made this app Possible. Thank you sincerely.   


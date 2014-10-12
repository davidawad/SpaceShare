from flask import *
from pymongo import MongoClient
import sys,os,sendgrid,twilio, gridfs,pymongo
from werkzeug import secure_filename
from flask.ext.pymongo import PyMongo

app=Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/upload/<path:spacenum>', methods=['GET'])
def edit_page(spacenum):	
    page = mongo.db.pages.find_one_or_404({'_id': spacenum})
    return render_template('page.html',page=page,spacenum=spacenum)

@app.route('/upload/<path:spacenum>', methods=['POST'])
def save_page(spacenum):
    mongo.db.pages.insert({'_id': spacenum, 'body': request.form['body']  }  )    
    return render_template('page.html', spacenum=spacenum)

@app.errorhandler(404)
def new_page(error):
    pagepath = request.path.lstrip('/')
    if pagepath.startswith('uploads'):
        filename = pagepath[len('uploads'):].lstrip('/')
        return render_template('upload.html', filename=filename)
    else:
        return render_template('edit.html', page=None, pagepath=pagepath)


if __name__ == '__main__':
    app.run(debug=True)


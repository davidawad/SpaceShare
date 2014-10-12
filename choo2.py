from flask import *
from pymongo import MongoClient
import sys,os,sendgrid,twilio, gridfs,pymongo
from werkzeug import secure_filename
from flask.ext.pymongo import PyMongo
from bson import BSON
##ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app=Flask(__name__)
mongo = PyMongo(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'
db = "spaceshare"
def get_db(): # get a connection to the db above
	conn = None
	try:
	    conn = pymongo.MongoClient()
	    print "Connected successfully!!!"
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e 
	   sys.exit(1)
	return conn[db]

# put files in mongodb
def put_file(file_location, room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	with open(file_location, "r") as f:
		gfs.put(f, room=room_number)

# read files from mongodb
def read_file(output_location, room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
	return gfs.get(_id).read()
	#with open(output_location, 'w') as f:
	#	f.write(gfs.get(_id).read())


@app.route('/HomePage')
def home():
	print 'hello'
	return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
	#get the name of the uploaded file
	tfile=request.files['file']
	#print "requested files" 
	spacenum=request.form['space']
	if tfile and spacenum :
		#import pdb; pdb.set_trace()
		try:
			mongo.db.files.insert({'_id': spacenum, 'body': request.files['file'].read()})
			return render_template('page.html',spacenum=spacenum)		
		except Exception:
			return render_template('error.html',spacenum=spacenum)

@app.route('/upload/<spacenum>', methods=['GET'])
def return_file(spacenum):	
	data = mongo.db.files.find_one({'_id': spacenum})['body']
	file_object = open(filename, w)
	filename.write(data)
	print filename
	filename.close()
	##print filename	
	return render_template('page.html',data=data, filename=filename,spacenum=spacenum)

@app.route('/get')
def getstuff():
	print 'getting stuff'
	spacenum=request.form['space'] 
	print spacenum
	redirect(url_for('/'))


if __name__ == '__main__':
	app.run(debug=True)

from flask import *
from pymongo import MongoClient
import sys,os,sendgrid,twilio, gridfs, pymongo ##will add sendgrid and twilio functionality.
from werkzeug import secure_filename
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
db = "spaceshare"
def get_db(): # get a connection to the db above
	conn = None
	try:
	    conn = pymongo.MongoClient()
	except pymongo.errors.ConnectionFailure, e:
	   print "Could not connect to MongoDB: %s" % e
	   sys.exit(1)
	return conn[db]

@app.route('/')
def home():
	return render_template('index.html')

# put files in mongodb
def put_file(file_name, room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	with open('uploads/' + file_name, "r") as f:
		gfs.put(f, room=room_number)

# read files from mongodb
def read_file(output_location, room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
	with open(output_location + str(room_number) , 'w') as f:
		f.write(gfs.get(_id).read())
	return gfs.get(_id).read()

def search_file(spacenum):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room=room_number))
	print _id

@app.route('/upload',methods=['POST'])
def upload():
	#get the name of the uploaded file
	file = request.files['file']
	#print "requested files"
	space = request.form['space']
	# if the file exists make it secure
	if file and space: #if the file exists
		# search to see if number is taken
		search_file(space)
		#make the file same, remove unssopurted chars
		filename=secure_filename(file.filename)
		#move the file to our uploads folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		put_file(filename,space)
		# remove the file from disk as we don't need it anymore after database insert.
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename))
		# debugging lines to write a record of inserts
		f = open('debug.txt', 'w')
		f.write('File name is '+filename+' the space is :'+ str(space) )
		return render_template('index.html', filename = filename ,space = space, up = True) ##take the file name
	else:
		return render_template('invalid.html')

@app.route('/upload/<spacenum>', methods=['GET'])
def download(spacenum):
	unSecurefilename = read_file(app.config['UPLOAD_FOLDER'] ,spacenum )
	render_template('index.html' , spacenum = spacenum)
	return send_from_directory(app.config['UPLOAD_FOLDER'], str(spacenum) )
	#remove from disk after file is given to user. use new thread to unlink??
	#os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , str( spacenum )))

@app.errorhandler(404)
def new_page(error):
	'''
	pagepath = request.path.lstrip('/')
	if pagepath.startswith('uploads'):
        	filename = pagepath[len('uploads'):].lstrip('/')
        	return render_template('upload.html', filename=filename)
    	else:
        	return render_template('edit.html', page=None, pagepath=pagepath)
	'''
if __name__ == '__main__':
	return render_template('error.html')
	app.run(debug=True)

	'''examples for gridfs functions
	file_location = "/Users/bedrich/Desktop/TODO-MCI"
	output_location = "/Users/bedrich/Desktop/omg"
	room_number = 12
	put_file(file_location, room_number)
	read_file(output_location, room_number)
	'''

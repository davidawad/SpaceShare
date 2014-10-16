from flask import *
from pymongo import MongoClient
import sys,os,sendgrid,twilio, gridfs,pymongo  ##will add sendgrid and twilio functionality.
from werkzeug import secure_filename
##ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app=Flask(__name__)
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
	#return gfs.get(_id).read()
	with open(output_location, 'w') as f:
		f.write(gfs.get(_id).read())


@app.route('/')
def home():
	return render_template('index.html')


@app.route('/upload',methods=['POST'])
def upload(): 
	#get the name of the uploaded file
	file=request.files['file']
	#print "requested files" 
	space=request.form['space']
	#print space
	# if the file exists make it secure
	print "space exists"
	if file: #if the file exists
		#make the file same, remove unssopurted chars
		filename=secure_filename(file.filename)
		#move the file to our uploads folder	
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		put_file(app.config['UPLOAD_FOLDER'],space)
		# remove the file from disk as we don't need it anymore after database insert. 
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename))
		# maybe redirect user to the uploaded_file route, which will show the uploaded file.
	print "running the upload process"

	##return render_template('space.html')	
	return render_template('page.html',filename=filename) ##this is wrong


@app.route('/uploads/<spacenum>', methods=['GET'])
def return_file(spacenum):
	print app.config['UPLOAD_FOLDER']
	print filename=
	read_file(app.config['UPLOAD_FOLDER'] ,spacenum)
	send_file(filename ,spacenum)
	#return render_template('Thanks.html',spacenum=spacenum,filename=filename)

##@app.route('/uploads/<filename>', methods=['GET'])
##def uploaded_file(filename):
#older implementation ideas  
##    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == '__main__':
	app.run(debug=True)
	file_location = "/Users/bedrich/Desktop/TODO-MCI"
	output_location = "/Users/bedrich/Desktop/omg"
	room_number = 12
	#put_file(file_location, room_number)
	#read_file(output_location, room_number)

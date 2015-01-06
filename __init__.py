from flask import *
from pymongo import MongoClient
import sys, os, gridfs, pymongo, time ##will add sendgrid and twilio functionality.
from werkzeug import secure_filename
from subprocess import Popen
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
db = "spaceshare"
# safety function to get a connection to the db above
def get_db():
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

# find if files exist
def search_file(room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room = room_number))
	return _id

#upload routine
@app.route('/upload',methods=['POST'])
def upload():
	#get the name of the uploaded file
	file = request.files['file']
	#print "requested files"
	space = request.form['space']
	# if file and space are given
	if file and space:
		# search to see if number is taken
		if search_file(space):
			render_template('index.html', space=space, taken=True)
		#make the file safe, remove unsupported chars
		filename = secure_filename(file.filename)
		#move the file to our uploads folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		# save file to mongodb
		put_file(filename,space)
		# debugging lines to write a record of inserts
		f = open('debug.txt', 'w')
		f.write('File name is :'+filename+', and the space is :'+ str(space) )
		render_template('index.html', space = space)
		time.sleep(600)
		# remove the file from disk as we don't need it anymore after 10 minutes
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename))
		return

	else:
		return render_template('invalid.html')

@app.route('/upload/<spacenum>', methods=['GET'])
def download(spacenum):
	unSecurefilename = read_file(app.config['UPLOAD_FOLDER'] ,spacenum )
	render_template('index.html' , spacenum = spacenum)
	return send_from_directory(app.config['UPLOAD_FOLDER'], str(spacenum) )
	#os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , str( spacenum )))

@app.route('/get')
def open_space():
	space = request.form['space']
	return redirect(url_for('/upload/'+str(space) ) )

@app.errorhandler(404)
def new_page(error):
	return render_template('index.html',non=True)
if __name__ == '__main__':
	app.run(debug=True)

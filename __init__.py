from flask import *
from pymongo import MongoClient
import sys, os, gridfs, pymongo, time ##will add sendgrid and twilio functionality.
from werkzeug import secure_filename
from random import randint
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
db = "spaceshare"

@app.route('/')
def home():
	return render_template('index.html')

# safety function to get a connection to the db above
def get_db():
	conn = None
	try:
	    conn = pymongo.MongoClient()
	except pymongo.errors.ConnectionFailure, e:
	   raise Exception("Could not connect to MongoDB: %s" % e)
	return conn[db]

# returns if space is taken
def search_file(room_number):
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	try:
		_id = db_conn.fs.files.find_one(dict(room = room_number))
	except Exception:
		_id = None
	if not _id:
		return False
	else:
		return True
#find a random integer not currently in the db
def find_number():
	while True:
		temp = randint(1,100) #inclusive
		if search_file(temp):
			continue
		else: ##we've found a random integer NOT already in the db, return
			return temp

# put files in mongodb
def put_file(file_name, room_number):
	if not(file_name and room_number):
		return
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	if search_file(room_number):
		print "space :"+str(room_number)+' is taken!'
		return
	try:
		with open('upload/' + file_name, "r") as f:
			gfs.put(f, room=room_number)
		print "Stored file :"+room_number+' Successfully'
	except Exception as e:
		print "File :"+'upload/'+file_name+" probably doesn't exist, : "+str(e)

# remove files from mongodb
def delete_file(room_number):
	if not(room_number):
		return
	if not search_file(room_number):
		print "file "+str(room_number)+' not in db, error?'
		return
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
	gfs.delete(_id)
	print "Deleted file :"+room_number+' Successfully'

# read files from mongodb
def read_file(output_location, room_number):
	if not(output_location and room_number):
		return
	if not search_file(room_number):
		print "file "+str(room_number)+' not in db, error?'
		return
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	try:
		_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
		with open('upload/' + str(room_number) , 'w') as f:
			f.write(gfs.get(_id).read())
		gfs.get(_id).read()
		print "Written file :"+room_number+' Successfully'
	except Exception as e:
		print "failed to read file :"+str(e)
		return False

#upload routine
@app.route('/upload',methods=['POST'])
def upload():
	#get the form inputs
	file = request.files['file']
	space = request.form['space']
	# if file and space are given
	if file and space:
		# search to see if number is taken
		if search_file(space):
			#space is taken, generate new available number
			new = find_number()
			render_template('index.html', space=space, new=new)
		#make the file safe, remove unsupported chars
		filename = secure_filename(file.filename)
		#move the file to our upload folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		# save file to mongodb
		put_file(filename,space)
		# debugging lines to write a record of inserts
		f = open('debug.txt', 'w')
		f.write('File name is :'+filename+', and the space is :'+ str(space) )
		#time.sleep(600)
		#remove the file from disk as we don't need it anymore after 10 minutes
		#os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename))
		return render_template('index.html', space = space, free=True)

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
	print "REDIRECT ON SERVER"
	return redirect(url_for('/upload/'+str(space) ) )

@app.errorhandler(404)
def new_page(error):
	return render_template('index.html',non=True)

if __name__ == '__main__':
	app.run(debug=True)

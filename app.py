from flask import *
from pymongo import MongoClient
import sys,sendgrid,twilio, gridfs,pymongo

app=Flask(__name__)

db = "spaceshare"
# get a connection to the db above
def get_db():
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
	with open(output_location, 'w') as f:
		f.write(gfs.get(_id).read())


@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/host')
def process():
	total = 0
	data = request.args['file'] ##request.args will grab the name attributed from
	space = request.args['space']
	if not request.args['pass'] :		##if there is no password then let's work with this 
		return render_template('space.html',space=space)
	print open(data,r)
	
	return render_template('space.html',space=space)

@app.route('/get')
def guest_book():


    return render_template('space.html')


if __name__ == '__main__':
	app.run(debug=True)
	file_location = "/Users/bedrich/Desktop/TODO-MCI"
	output_location = "/Users/bedrich/Desktop/omg"
	room_number = 12
	put_file(file_location, room_number)
	#read_file(output_location, room_number)

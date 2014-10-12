import pymongo
import gridfs
import sys

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

if __name__ == "__main__":
	file_location = "/Users/bedrich/Desktop/TODO-MCI"
	output_location = "/Users/bedrich/Desktop/omg"
	room_number = 12
	# put_file(file_location, room_number)
	read_file(output_location, room_number)



from flask import *
from pymongo import MongoClient
import os, gridfs, pymongo, time, logging , sendgrid
from werkzeug import secure_filename
from random import randint

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
	if not os.path.exists('upload/'):
		try:
			os.makedirs('upload/')
		except Exception as e:
			logger.info( e )
	return render_template('index.html')

# safety function to get a connection to the db above
def get_db():
	try:
		uri = os.environ.get('MONGOLAB_URI', 'mongodb://localhost')
		conn = MongoClient(uri)
		db = conn.heroku_app33243434
		collection = db.santa
		return db
	except pymongo.errors.ConnectionFailure, e:
	   raise Exception("Could not connect to MongoDB: %s" % e)

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
def insert_file(file_name, room_number):
	if not(file_name and room_number):
		return
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	if search_file(room_number):
		logger.info( "Space :"+ str(room_number) + ' is taken!' )
		return False
	try:
		with open('upload/' + file_name, "r") as f:
			#write bytes of the file into the gfs database
			gfs.put(f, room=room_number, name=file_name)
		logger.info( "Stored file : "+str(room_number)+' Successfully')
		return True
	except Exception as e:
		logger.info( "File :"+'upload/'+file_name+" probably doesn't exist, : "+str(e) )
		return False

# remove files from mongodb
def delete_file(room_number):
	if not(room_number):
		raise Exception("delete_file given None")
	if not search_file(room_number):
		logger.info( "File "+str(room_number)+' not in db, error?' )
		return True
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
	gfs.delete(_id)
	logger.info( "Deleted file :"+str(room_number)+' Successfully' )
	return True

# read files from mongodb
def extract_file(output_location, room_number):
	if not(output_location and room_number):
		raise Exception("extract_file not given proper values")
	if not search_file(room_number):
		logger.info( "File "+str(room_number)+' not in db, error?' )
		return False
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	try:
		_id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
		file_name = db_conn.fs.files.find_one(dict(room=room_number))['name']
		with open('upload/' + file_name , 'w') as f:
			f.write(gfs.get(_id).read())
		gfs.get(_id).read() # not sure why this line is here.
		logger.info( "Written file :"+str(room_number)+' Successfully' )
		return True
	except Exception as e:
		logger.info( "failed to read file :"+str(e) )
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
			return render_template('index.html', space=space, new=new)
		#make the file safe, remove unsupported chars
		filename = secure_filename(file.filename)
		logger.info('Securing Filename: '+filename)
		#move the file to our upload folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		logger.info('File '+filename+' saved.')
		# save file to mongodb
		res = insert_file(filename,space)
		logger.info('Inserted '+ filename +' to db at position: '+str(space) )
		# upload failed for whatever reason
		if not res:
			os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename ))
			return render_template('index.html', space=space, failed=True)
		if app.debug:
			# debugging lines to write a record of inserts
			with open('debug.txt', 'w') as f:
				f.write('File name is : '+filename+', and the space is : '+ str(space) )
		# file upload successful, remove copy from disk.
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] ,  filename  ))
		return render_template('index.html', space=space, upload=True)
	else: # something went wrong then! yes, indeed,
		return render_template('invalid.html')
	@after_this_request
	def expire_file():
		logger.info("AFTER REQUEST HAPPENING.")
		# wait 10 minutes,
		time.sleep(600)
		delete_file(space)
		try:  #attempt to unlink just in case.
			os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , filename ))
		except Exception:
			return
		return

@app.route( '/upload/<spacenum>' , methods=['GET'])
def download(spacenum):
	logger.info("Entering server redirect!")
	# check it's in there
	if not search_file(spacenum):
		logger.info( "File "+str(spacenum)+' not in db, error?' )
	# render the template
	render_template('index.html' , spacenum = spacenum)
	logger.info("Connecting to DB")
	# connect to mongo
	db_conn = get_db()
	gfs = gridfs.GridFS(db_conn)
	file_name = db_conn.fs.files.find_one(dict(room=spacenum))['name']
	logger.info("File name is : "  +file_name + " !")
	#extract file to send from directory
	extract_file(app.config['UPLOAD_FOLDER'] , spacenum )
	# send the file we just created
	response = send_file(app.config['UPLOAD_FOLDER']+file_name)
	return response
	@after_this_request
	def clean_file(response):
		# clean the file after it's served.
		logger.info( 'Response is : '+response)
		os.unlink(os.path.join( app.config['UPLOAD_FOLDER'] , file_name  ))
		return

@app.errorhandler(404)
def new_page(error):
	return render_template('error.html', error=404)

@app.errorhandler(500)
def page_not_found(error): # will send me an email with hopefully some relevant information using sendgrid
	sg = sendgrid.SendGridClient('YOUR_SENDGRID_USERNAME', 'YOUR_SENDGRID_PASSWORD')
	message = sendgrid.Mail()
	message.add_to('David Awad <davidawad64@gmail.com>')
	message.set_subject('500 Error on Spaceshare')
	message.set_html('Body')
	message.set_text('Hey dave, there was another error on spaceshare I apologize! Spaceshare currently has '+str(visitors)+' visitors.')
	message.set_from('Space Admin <Admin@spaceshare.me>')
	#status, msg = sg.send(message)
	return render_template('error.html', error=500)

if __name__ == '__main__':
	app.run(debug=True)

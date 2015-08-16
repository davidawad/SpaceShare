from flask import request, render_template, Blueprint, jsonify
from werkzeug import secure_filename
from pymongo import MongoClient
from random import randint
from config import config
# from tasks import print_words
import gridfs
import pymongo
import time
import logging
import sendgrid
import os


app = Blueprint('app', __name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


db_conn = None


# safety function to get a connection to the db above
def get_db():
    try:
        logger.info("Connecting to db ..." + str(db_conn))
    except Exception as e:
        db_conn = None
    if not db_conn:
        try:
            uri = os.environ.get('MONGOLAB_URI', 'mongodb://localhost')
            conn = MongoClient(uri)
            db = conn.heroku_app33243434
            db_conn = db
        except pymongo.errors.ConnectionFailure, e:
            logger.critical("Could not connect to MongoDB: %s" % e)
    return db_conn


# returns if space is taken
def search_file(room_number):
    db_conn = get_db()
    try:
        return db_conn.fs.files.find_one(dict(room=room_number))
    except Exception:
        return False


# find an integer not currently taken in db
def find_number():
    db_conn = get_db()
    '''
    The empty dict in the first argument means "give me every document in the
    database"
    The "fields=['room']" in the second argument says "of those documents, only
    populate the 'room' field." This is to cut down on the size of response.
    The list comprehension pulls the value from the "room" field from each dict
    in the list of dicts returned by find().
    '''
    rooms_in_db = [doc["room"] for doc in db_conn.fs.files.find({}, fields=["room"])]
    room_not_in_db = int(max(rooms_in_db)) + 1
    return room_not_in_db


# put files in mongodb
def insert_file(file_name, room_number):
    if not(file_name and room_number):
        return
    db_conn = get_db()
    gfs = gridfs.GridFS(db_conn)
    if search_file(room_number):
        logger.info("Space :" + str(room_number) + ' is taken!')
        return False
    try:
        with open('upload/' + file_name, "r") as f:
            # write bytes of the file into the gfs database
            gfs.put(f, room=room_number, name=file_name)
        logger.info("Stored file : "+str(room_number)+' Successfully')
        return True
    except Exception as e:
        logger.info("File :"+'upload/'+file_name+" probably doesn't exist, : "
                    + str(e))
        return False


# remove files from mongodb
def delete_file(room_number):
    if not(room_number):
        raise Exception("delete_file given None")
    if not search_file(room_number):
        logger.info("File "+str(room_number)+' not in db, error?')
        return True
    db_conn = get_db()
    gfs = gridfs.GridFS(db_conn)
    _id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
    gfs.delete(_id)
    logger.info("Deleted file :"+str(room_number)+' Successfully')
    return True


# read files out of mongodb
def extract_file(output_location, room_number):
    if not(output_location and room_number):
        raise Exception("extract_file not given proper values")
    if not search_file(room_number):
        logger.info("File "+str(room_number)+' not in db, error?')
        return False
    db_conn = get_db()
    gfs = gridfs.GridFS(db_conn)
    try:
        _id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
        file_name = db_conn.fs.files.find_one(dict(room=room_number))['name']
        # read gridFS binary blob from mongo, write the file
        with open('upload/' + file_name, 'w') as f:
            f.write(gfs.get(_id).read())
        # gfs.get(_id).read()
        logger.info("Written file :"+str(room_number)+' Successfully')
        return True
    except Exception as e:
        logger.info("failed to read file :"+str(e))
        return False


# upload routine
@app.route('/upload', methods=['POST'])
def upload():
    # get the form inputs
    file = request.files['file']
    space = request.form['space']
    # if file and space are given
    if file and space:
        # search to see if number is taken
        if search_file(space):
            # space is taken, generate new available number
            new = find_number()
            return render_template('index.html', space=space, new=new)
        # make the file safe, remove unsupported chars
        filename = secure_filename(file.filename)
        logger.info('Securing Filename: '+filename)
        # move the file to our upload folder
        file.save(os.path.join(config['UPLOAD_FOLDER'], filename))
        logger.info('File '+filename+' saved.')
        # save file to mongodb
        res = insert_file(filename, space)
        logger.info('Inserted '+filename+' to db at position: '+str(space))
        # upload failed for whatever reason
        if not res:
            os.unlink(os.path.join(config['UPLOAD_FOLDER'], filename))
            return render_template('index.html', space=space, failed=True)
        if app.debug:
            # debugging lines to write a record of inserts
            # TODO add this to the log instead
            with open('debug.txt', 'w') as f:
                f.write('File name is : '+filename+', and the space is : ' +
                        str(space))
        # file upload successful, remove copy from disk.
        os.unlink(os.path.join(config['UPLOAD_FOLDER'],  filename))
        return render_template('index.html', space=space, upload=True)
    else:  # something went wrong then! yes, indeed,
        return render_template('error.html')


# download routine
@app.route('/upload/<spacenum>', methods=['GET'])
def download(spacenum):
    logger.info("Entering server redirect!")
    # check it's in there
    if not search_file(spacenum):
        logger.info("File "+str(spacenum)+' not in db, error?')
        # return error or 404, or something, we have no file.
        return render_template('index.html', undef=True, space=spacenum)
    # render the template
    render_template('index.html', spacenum=spacenum)
    logger.info("Connecting to DB")
    # connect to mongo
    db_conn = get_db()
    gfs = gridfs.GridFS(db_conn)
    file_name = db_conn.fs.files.find_one(dict(room=spacenum))['name']
    logger.info("File name is : "+file_name + " !")
    # extract file to send from directory
    extract_file(config['UPLOAD_FOLDER'], spacenum)
    # send the file we just created
    response = send_file(config['UPLOAD_FOLDER']+file_name)
    return response
    # TODO append to celery task queue

if __name__ == '__main__':
    app.run(
        debug=config['DEBUG'],
        threaded=True,
        port=4000
        )

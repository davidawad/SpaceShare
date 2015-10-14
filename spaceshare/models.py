##
# This file defines our celery tasks
# essentially functions that we can call from our route handlers
# These functions can run in the background and deal with handling
# tasks transparently to the user and behind the application
# In this case these are our models
#
# @author David Awad

from flask import request, render_template, Blueprint, jsonify
from werkzeug import secure_filename
from pymongo import MongoClient
from random import randint
from config import config
from celery import Celery
import gridfs
import pymongo
import time
import logging
import os

# add a blueprint for our functions
blueprint_app = Blueprint('app', __name__)

# configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery
celery = Celery(config['NAME'], broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)

# cache a db connection in memory
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


@celery.task(bind=True)
def search_file(self, spacenum):
    # TODO doesn't necessarily need to be async?
    if not spacenum:
        # just assume this integer is taken. correct outside
        return True
    # searches for an int and returns if the space is taken
    if config['DEBUG']:
        if spacenum == 64:
            # special debug value
            return True
    try:
        db_conn = get_db()
        if db_conn.fs.files.find_one(dict(room=spacenum)):
            return True
        else:
            return False
    except Exception:
        return False


@celery.task(bind=True)
def find_number(self):
    '''
    find an integer not currently taken in db

    The empty dict in the first argument means "give me every document in the
    database"
    The "fields=['room']" in the second argument says "of those documents, only
    populate the 'room' field." This is to cut down on the size of response.
    The list comprehension pulls the value from the "room" field from each dict
    in the list of dicts returned by find().
    '''
    db_conn = get_db()
    if not db_conn:
        logger.error("couldn't get db connection")
        return None
    rooms_in_db = [doc["room"] for doc in db_conn.fs.files.find({}, fields=["room"])]
    room_not_in_db = int(max(rooms_in_db)) + 1
    logger.info("found largest entry: "+str(rooms_in_db))
    return room_not_in_db

# TODO refactor for data_URI strings
@celery.task(bind=True)
def insert_file(self, file_name, room_number):
    # make sure we're given file_name and number
    if not(file_name and room_number):
        return
    # then check if that int is taken
    if search_file(room_number):
        logger.info("Space :" + str(room_number) + ' is taken!')
        return False
    # we know we should store the file now
    db_conn = get_db()
    gfs = gridfs.GridFS(db_conn)
    try:
        with open('upload/' + file_name, "r") as f:
            # write bytes of the file into the gfs database
            gfs.put(f, room=room_number, name=file_name)
        logger.info("Stored file : "+str(room_number)+' Successfully')
        return True
    except Exception as e:
        logger.info("File :"+'upload/'+file_name+" probably doesn't exist, : " + str(e))
        return False


@celery.task(bind=True)
def delete_file(self, room_number):
    # remove file from mongo
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


@celery.task(bind=True)
def extract_file(self, output_location, room_number):
    # extract file from mongo and throw it in the uploads
    if not(output_location and room_number):
        # FIXME this probably shouldn't be an exception,
        # should maybe be refactored
        raise Exception("extract_file not given proper values")
    if not search_file(room_number):
        logger.info("File "+str(room_number)+' not in db, error?')
        return False
    try:
        db_conn = get_db()
        gfs = gridfs.GridFS(db_conn)
        _id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
        file_name = db_conn.fs.files.find_one(dict(room=room_number))['name']
        # read gridFS binary blob from mongo, write the file
        logger.info("extracting file: "+file_name)
        with open('upload/' + file_name, 'w') as f:
            f.write(gfs.get(_id).read())
        # gfs.get(_id).read()
        logger.info("Written file :"+str(room_number)+' Successfully')
        return True
    except Exception as e:
        logger.info("failed to read file :"+str(e))
        return False


# upload routine
@blueprint_app.route('/upload', methods=['POST'])
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


if __name__ == '__main__':
    app.run(
        debug=config['DEBUG'],
        threaded=True,
        port=4000
        )

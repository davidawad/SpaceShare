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
    global db_conn
    if db_conn:
        return db_conn

    else:
        try:
            conn = MongoClient(os.environ.get('DB_PORT_27017_TCP_ADDR', 'localhost'),
                    27017)
            # conn.spaceshare.files.find()
            db_conn = conn
            return db_conn
        except pymongo.errors.ConnectionFailure as e:
            logger.critical("Could not connect to MongoDB: %s" % e)
            return False


def space_taken(spacenum):
    '''
    searches for a given integer in the database
    and returns True if the space is taken.

    if not passed a number, assume taken
    '''
    if not spacenum:
        return True
    if config['DEBUG']:
        logger.info("space_taken passed " + str(spacenum))
        # special debug value of 64
        if int(spacenum) == 64:
            return True
    try:
        db_conn = get_db()
        # TODO fix this db connection
        rooms_in_db = [doc["space"] for doc in db_conn.spaceshare.files.find()]
        for num in rooms_in_db:
            if spacenum == num:
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
    try:
        db_conn = get_db()
        # TODO debug find_numbers
        rooms_in_db = [doc["space"] for doc in db_conn.spaceshare.files.find()]
        logger.info(rooms_in_db)
        print(rooms_in_db)
        free_space = int(max(rooms_in_db)) + 1
        logger.info("found largest entry: " + str(free_space))
        return free_space
    except Exception as e:
        logger.error(str(e))
        return None

'''
# TODO refactor for data_URI strings
@celery.task(bind=True)
def insert_file(self, file_name, room_number):
    # make sure we're given file_name and number
    if not(file_name and room_number):
        return
    # then check if that int is taken
    if space_taken(room_number):
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
        logger.info("File :"+'upload/'+file_name+" probably doesn't exist, : "+str(e))
        return False
'''


def delete_file(space):
    # remove file from mongo
    if not space:
        logger.error("delete_file given None")
        return True
    if not space_taken(space):
        logger.info("File " + str(room_number) + ' not in db, error')
        return True
    try:
        db_conn = get_db()
        result = conn.spaceshare.files.remove({'space': space})
        if result <= 1:
            logger.error("Failed to delete file :" + str(space))
            return False
        # assume success
        logger.info("Deleted file :" + str(space) + ' Successfully')
        return True
    except Exception as e:
        logger.error("Couldn't delete file at space " + space + ':' + str(e))
        return False


@celery.task(bind=True)
def extract_file(self, room_number):
    # extract file from mongo and throw it in the uploads
    if not room_number:
        # FIXME this probably shouldn't be an exception,
        # should maybe be refactored
        raise Exception("extract_file not given proper values")
    if not space_taken(room_number):
        logger.info("File " + str(room_number) + ' not in db, error?')
        return False
    try:
        db_conn = get_db()
        gfs = gridfs.GridFS(db_conn)
        _id = db_conn.fs.files.find_one(dict(room=room_number))['_id']
        file_name = db_conn.fs.files.find_one(dict(room=room_number))['name']
        # read gridFS binary blob from mongo, write the file
        logger.info("extracting file: " + file_name)
        with open(config['UPLOAD_FOLDER'] + file_name, 'w') as f:
            f.write(gfs.get(_id).read())
        # gfs.get(_id).read()
        logger.info("Written file :" + str(room_number) + ' successfully')
        return True
    except Exception as e:
        logger.info("failed to read file :" + str(e))
        return False


def insert_file(file_obj):
    '''
    Take files as a data_URI and store them in a mongoDB.
    '''
    # TODO one time uploads and time based removals
    db_conn = get_db()

    if space_taken(file_obj):
        logger.error('SPACE TAKEN IN MODEL FUNCTION')
        return False

    res_id = db_conn.spaceshare.files.insert_one(file_obj)
    # upload failed for whatever reason
    if not res_id:
        return False
    if config['DEBUG']:
        # debugging lines to write a record of inserts
        logger.info('Passed file: ' + filename + ' stored at space ' + space + '.')

    return True

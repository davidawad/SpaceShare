##
# This file defines our routes and their controllers functions
# These are the functions that validate user input when it's
# first given to spaceshare.
# In this case these are our controllers that handle the routing logic
#
# @author David Awad

from flask import request, Blueprint, jsonify
from werkzeug import secure_filename
from config import config
from models import *
import logging

# set up blueprint for controllers
blueprint_api = Blueprint('blueprint_api', __name__)

# configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@blueprint_api.route('/_find_number', methods=['GET'])
def request_find_number():
    try:  # return the json result, the empty numbered room
        logger.info('request at /find_number')
        return jsonify(result=find_number.apply_async().get())
    except Exception as e:
        logger.error("error on JSON request find_number: "+str(e))
        return jsonify(result="error on JSON request find_number: "+str(e))


@blueprint_api.route('/_route_taken', methods=['GET'])
def request_route_taken():
    unused = 0
    request_space = request.args['space']
    try:  # return the json result, the empty numbered room
        result = space_taken(request_space)
        logger.info('/route_taken?space='+str(request_space)+' response:'+str(result))
        ret = jsonify(result=result)
        return ret
    except Exception as e:
        logger.error("error on JSON /api/_route_taken: "+str(e))
        return jsonify(result="error on route_taken for input "+str(request_space))


@blueprint_api.route('/download/<spacenum>', methods=['GET'])
def download(spacenum):
    if not models.space_taken(spacenum):
        logger.info("File "+str(spacenum)+' not in db, error?')
        # return error or 404, or something, we have no file.
        return render_template('error.html',
                               error="file :"+spacenum+" doesn't exist")
    # extract file to send from directory
    result = extract_file.apply_async([spacenum]).get()
    if not result:
        # render a template with this updated information
        render_template('error.html', error="file couldn't be served")
    # send the file we just created
    response = send_file(config['UPLOAD_FOLDER']+file_name)
    return response


@blueprint_api.route('/upload_file', methods=['POST'])
def upload():
    # get the form inputs
    file_name = request.files['name']
    space = int(request.form['space'])
    data_uri = request.form['data_uri']
    # if file and space are given
    if file_name and space and data_uri:
        # search to see if number is taken
        if space_taken(space):
            # space is taken, use new available number
            space = find_number()
        # make the file safe, remove unsupported chars
        file_name = secure_filename(file_name)
        logger.info('Uploaded File: '+filename)
        # throw file into DB. Hope it works
        if not insert_file.apply_async([file_name, space, data_uri]).get():
            return jsonify(error="file couldn't be uploaded, please try again")

        # upload succeeded
        return jsonify(result="file uploaded!", space=space)

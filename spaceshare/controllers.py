##
# This file defines our routes and their controllers functions
# These are the functions that validate user input when it's
# first given to spaceshare.
# In this case these are our controllers that handle the routing logic
#
# @author David Awad

from flask import request, Blueprint, jsonify
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
    unused = 0
    try:  # return the json result, the empty numbered room
        ret = jsonify(result=find_number.apply_async().get())
        logger.info('given request at find_number, returning' + str(ret))
        return ret
    except Exception as e:
        logger.error("error on JSON request find_number: "+str(e))
        return


@blueprint_api.route('/_route_taken', methods=['GET'])
def request_route_taken():
    unused = 0
    request_space = request.args['space']
    # logger.info('checking space '+str(request_space))
    try:  # return the json result, the empty numbered room
        result = search_file.apply_async([request_space])
        logger.info('/route_taken?space='+str(request_space)+' response:'+str(result.get()))
        ret = jsonify(result=result.get())
        # logger.info('given request at _route_taken, returning' + str(re))
        return ret
    except Exception as e:
        logger.error("error on JSON /api/_find_number: "+str(e))
        return jsonify(result="error on route_taken for input "+str(request_space))


# download routine
@blueprint_api.route('/upload/<spacenum>', methods=['GET'])
def download(spacenum):
    logger.info("Entering server redirect!")
    # check it's in there
    if not models.search_file(spacenum):
        logger.info("File "+str(spacenum)+' not in db, error?')
        # return error or 404, or something, we have no file.
        return render_template('index.html', undef=True, space=spacenum)
    # number is there
    logger.info("Connecting to DB")
    # extract file to send from directory
    written = models.extract_file(config['UPLOAD_FOLDER'], spacenum)
    if not written:
        # render a template with this updated information
        render_template('error.html', error="file couldn't be served")
    # send the file we just created
    response = send_file(config['UPLOAD_FOLDER']+file_name)
    return response

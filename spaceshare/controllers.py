##
# This file defines our routes and their controllers functions
# These are the functions that validate user input when it's
# first given to spaceshare.
# In this case these are our controllers
#
# @author David Awad

from flask import request, Blueprint, jsonify
from config import config
import app

api = Blueprint('api', __name__)


@api.route('/_find_number', methods=['GET'])
def request_find_number():
    unused = 0
    try:  # return the json result, the empty numbered room
        ret = jsonify(result=models.find_number())

    except Exception as e:
        logger.error("error on JSON request find_number: "+str(e))
        return


@api.route('/_route_taken', methods=['GET'])
def request_route_taken():
    unused = 0
    request_space = request.args['space']
    try:  # return the json result, the empty numbered room
        ret = jsonify(result=models.search_file(request_space))
        return ret
    except Exception as e:
        logger.error("error on JSON request find_number: "+str(e))
        return jsonify(result="error on route taken")


# download routine
@api.route('/upload/<spacenum>', methods=['GET'])
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

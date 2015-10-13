from flask import request, Blueprint, jsonify
from config import config

api = Blueprint('api', __name__)


# Route that will process the AJAX request,
# result as a proper JSON response with a currently free int in the database
@api.route('/_find_number')
def request_find_number():
    unused = 0
    if config['DEBUG']:
        return jsonify(result=64)
    try:  # return the json result, the empty numbered room
        return jsonify(result=find_number())
    except Exception as e:
        logger.error("error on JSON request find_number: "+str(e))
        return

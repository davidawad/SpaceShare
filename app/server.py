##
# This file defines our webserver level configurations
#
# @author David Awad
from flask import Flask, Request, render_template, request, jsonify
from controllers import blueprint_api
from models import blueprint_app
from config import config
import mandrill
import logging
import sys
import os


application = Flask(__name__)
# FIXME set url prefix for celery tasks
application.register_blueprint(blueprint_app)
application.register_blueprint(blueprint_api, url_prefix='/api')

logger = logging.getLogger(__name__)


# update config from yaml dict
for key in config.keys():
    application.config.update(key=config[key])

# write logs to a file for production
if config['DEBUG'] is not True:
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    application.logger.addHandler(file_handler)

# if the upload folder doesn't exist we've just started the application.
if not os.path.exists(config['UPLOAD_FOLDER']):
    logger.error("upload folder didn't exist, creating it now")
    try:
        os.makedirs(config['UPLOAD_FOLDER'])
    except Exception as e:
        logger.info(e)


# will happlicationen before every request made to SpaceShare
@application.before_request
def before_request():
    return


# currently not supported
@application.route('/login')
def login():
    abort(401)


# route to the root directory
@application.route('/')
def home():
    return render_template('index.html')

if config['DEBUG']:
    # experimental reactJS page
    @application.route('/react')
    def reactions():
        return render_template('react-experiment.html')

    @application.route('/react/task/')
    def yolo():
        task = print_words.applicationly_async()
        response = {'task_id': task.id,
                    'progress': 'TASK_ACCEPTED'
                    }
        return jsonify(response)

    @application.route('/react/task/<task_id>')
    def yolo_again(task_id):
        print('task status request received ' + str(task_id))
        task = print_words.AsyncResult(task_id)
        print ("task state : " + task.state)
        if task.state == 'PENDING':
                # job did not start yet
                response = {
                    'state': task.state,
                    'current': 0,
                    'status': 'Pending...'
                }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'current': task.info.get('current', 0),
                'status': task.info.get('status', 'printing words...')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:
            # something went wrong in the background job
            response = {
                'state': task.state,
                'current': 1,
                'status': str(task.info),  # this is the exception raised
            }
        return jsonify(response)


@application.errorhandler(404)
def new_page(error):
    return render_template('error.html', error=404)


@application.errorhandler(405)
def new_page(error):
    return render_template('error.html', error=405)


@application.errorhandler(500)
def page_not_found(error):  # wake me in middle of the night
    send_error_report()
    return render_template('error.html', error=500)


def send_error_report():
    # TODO USE FLASK SMTP. DON'T PAY FOR THIS CRAP.
    try:
        logger.info(result)

    except Exception as e:  # Mandrill errors are thrown as exceptions
        logger.error('A mandrill error occurred: %s - %s' % (e.__class__, e))


if __name__ == '__main__':
    application.run(
        debug=config['DEBUG'],
        use_reloader=True,
        threaded=True,
        port=4000
        )

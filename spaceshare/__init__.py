from flask import Flask, Request, render_template, request
from app import app as base_app
from config import config
from api import api
import mandrill
import logging
import os


app = Flask(__name__)
app.register_blueprint(base_app)
app.register_blueprint(api, url_prefix='/api')

logger = logging.getLogger(__name__)


# update config from yaml dict
for key in config.keys():
    app.config.update(key=config[key])

# write logs to a file for production
if config['DEBUG'] is not True:
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

# if the upload folder doesn't exist we've just started the app.
if not os.path.exists(config['UPLOAD_FOLDER']):
    logger.error("upload folder didn't exist on up")
    try:
        os.makedirs(config['UPLOAD_FOLDER'])
    except Exception as e:
        logger.info(e)


# will happen before every request made to SpaceShare
@app.before_request
def before_request():
    return


# currently not supported
@app.route('/login')
def login():
    abort(401)


# route to the root directory
@app.route('/')
def home():
    return render_template('index.html')

if config['DEBUG']:
    # experimental reactJS page
    @app.route('/react')
    def reactions():
        return render_template('react-experiment.html')



@app.errorhandler(404)
def new_page(error):
    return render_template('error.html', error=404)


@app.errorhandler(405)
def new_page(error):
    return render_template('error.html', error=405)


@app.errorhandler(500)
def page_not_found(error):  # wake me in middle of the night
    send_error_report()
    return render_template('error.html', error=500)


def send_error_report():
    try:
        mandrill_client = mandrill.Mandrill(config['MANDRILL_KEY'])
        message = {'auto_html': None,
                   'auto_text': None,
                   'from_email': '',
                   'from_name': '',
                   'subject': '500 Error on Route' + str(request.base_url),
                   'text': 'Master! It appears someone caused an internal error. :' + str(request),
                   'to': [{'email': config['MANDRILL_ADDRESS'],
                          'name': config['MANDRILL_ADDRESS_NAME'],
                           'type': 'to'}],
                   }

        result = mandrill_client.messages.send(message=message,
                                               async=False,
                                               ip_pool='Main Pool',
                                               send_at='2012-01-05 12:42:01')
        logger.info(result)

    except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
        logger.error('A mandrill error occurred: %s - %s' % (e.__class__, e))


if __name__ == '__main__':
    app.run(
        debug=config['DEBUG'],
        use_reloader=True,
        threaded=True,
        port=4000
        )

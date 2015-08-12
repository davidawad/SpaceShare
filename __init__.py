from flask import Flask, Request, render_template, request
from app import app as base_app
from config import config
from api import api
import mandrill
import logging
import os


logger = logging.getLogger(__name__)

app = Flask(__name__)

# update config from yaml dict
for key in config.keys():
    app.config.update(key=config[key])

app.register_blueprint(base_app)
app.register_blueprint(api, url_prefix='/api')


@app.before_request
def before_request():
    print 'request received'
    return


@app.route('/login')
def login():
    abort(401)


# route to the root directory
@app.route('/')
def home():
    if not os.path.exists('upload/'):
        logger.error("upload folder didn't exist on up")
        try:
            os.makedirs('upload/')
        except Exception as e:
            logger.info(e)
    return render_template('index.html')


'''
# FIXME apply this in a celery task queue
@after_this_request
def expire_file():
    logger.info("AFTER REQUEST HAPPENING.")
    # wait 10 minutes,
    time.sleep(600)
    delete_file(space)
    try:  # attempt to unlink just in case.
        os.unlink(os.path.join(config['UPLOAD_FOLDER'], filename))
    except Exception:
        return
    return
'''


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
                   'from_email': 'FleetDirac@rsglab.com',
                   'from_name': 'Dirac',

                   'subject': 'example subject',
                   'text': 'It appears someone caused an internal error. :' + str(request),
                   'to': [{'email': config['MANDRILL_ADDRESS'],
                          'name': config['MANDRILL_ADDRESS_NAME'],
                           'type': 'to'}],
                   }

        result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool', send_at='2012-01-05 12:42:01')
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

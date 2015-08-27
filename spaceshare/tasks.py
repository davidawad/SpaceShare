from config import config
from flask import jsonify
from celery import Celery
import time

##
# This file defines our celery tasks
# essentially functions that we can call from our route handlers
# These functions can run in the background and deal with handling
# tasks transparently to the user and behind the application
#


# Initialize Celery
celery = Celery(config['NAME'], broker=config['CELERY_BROKER_URL'])
celery.conf.update(config)


# with bind = true we can monitor the progress of the celery process
@celery.task(bind=True)
def print_words(self):
    # some long task that does work
    for i in range(23):
        print 'words'
        time.sleep(1)
        # update metadata variables
        self.update_state(state='PENDING',
                          meta={'current': i,
                                'status': 'counting'
                                }
                          )

    self.update_state(state='FINISHED',
                      meta={'current': i,
                            'status': 'counting'
                            }
                      )
    return 100023


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}

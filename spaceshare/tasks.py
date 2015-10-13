from config import config
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
        print 'words' + str(i)
        time.sleep(1)
        # update metadata variables
        self.update_state(state='PROCESSING',
                          meta={'current': i,
                                'status': 'counting ...'
                                }
                          )

    self.update_state(state='FINISHED',
                      meta={'current': i,
                            'status': 'counting'
                            }
                      )
    return 100023

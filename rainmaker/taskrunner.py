import time

import rainmaker.stats

def jury_rigged_celery():
    while 1 > 0:
        rainmaker.stats.save_lending_stats()
        time.sleep(10)

jury_rigged_celery()
import time

import rainmaker.stats

def jury_rigged_celery():
    print 'CALLED JURY RIGGED CELERY'
    while 1 > 0:
        rainmaker.stats.save_lending_stats()
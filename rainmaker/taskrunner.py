import time

import rainmaker.stats

while 1 > 0:
    rainmaker.stats.save_lending_stats()
    time.sleep(10)
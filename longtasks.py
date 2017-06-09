import logging
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
import time
import datetime
from django.utils import timezone
import decimal

import poloapi.restapi
from rainmaker.models import LendHistory, LendStats
from rainmaker.utils import BitcoinDecimal


freqency = 10  # seconds
seconds_in_day = 86400
num_loops = (seconds_in_day / freqency)


def save_lending_stats():
    for x in xrange(num_loops):
        last_cycle = LendStats.objects.last()
        if not last_cycle:
            logging.debug('No Previous LendStats entry found.')
        time_since_last = timezone.now() - last_cycle.created_at
        if time_since_last < datetime.timedelta(seconds=9):
            logging.warning('Save fired too quickly since last save. Time since last save {}'.format(
                time_since_last.seconds))
            time.sleep(1)
        p = poloapi.restapi.poloniex()
        objects_list = []
        bid_asks = []
        loans = p.returnLoanOrders('BTC')['offers']
        i = 0
        for loan in loans:
            i += 1
            percent = decimal.Decimal(loan['rate']) * 100
            amount = BitcoinDecimal(loan['amount'])
            objects_list.append(LendHistory(amount=amount,
                                            interest_ask=percent))
            if i > 25:
                bid_asks.append(percent)
        LendHistory.objects.bulk_create(objects_list)
        avg_low_bid = sum(bid_asks) / len(bid_asks)
        LendStats.objects.create(avg_interest_ask=avg_low_bid)
        logging.info('Save completed at price: {}'.format(avg_low_bid))
        print 'Save completed at price: {}'.format(avg_low_bid)
        time.sleep(10)

if __name__ == '__main__':
    save_lending_stats()
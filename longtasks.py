import os

import logging
import threading

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import datetime
from django.utils import timezone
from django.db.transaction import atomic
import decimal

import poloapi.restapi
from rainmaker.models import LendHistory, LendStats
from rainmaker.utils import BitcoinDecimal

# freqency = 10  # seconds
# seconds_in_2day = 86400 * 2
# num_loops = (seconds_in_2day / freqency)


@atomic
def save_lending_stats():
    last_cycle = LendStats.objects.last()
    if not last_cycle:
        logging.debug('No Previous LendStats entry found.')
    time_since_last = timezone.now() - last_cycle.created_at
    if time_since_last < datetime.timedelta(seconds=9):
        logging.warning('Save fired too quickly since last save. Time since last save {}'.found(
            time_since_last.seconds))
        return
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


class perpetualTimer():
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = threading.Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = threading.Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()


t = perpetualTimer(10.0, save_lending_stats)
t.start()

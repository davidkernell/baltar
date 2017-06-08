import os

import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import datetime
from django.utils import timezone
from django.db.transaction import atomic
import decimal
import time

import poloapi.restapi
from rainmaker.models import LendHistory, LendStats
from rainmaker.utils import BitcoinDecimal


def save_lending_stats():
    freqency = 10  # seconds
    seconds_in_2day = 86400 * 2
    num_loops = (seconds_in_2day / freqency)
    for x in xrange(num_loops):
        logging.info('Save Called: {} loop'.format(x))
        with atomic():
            last_cycle = LendStats.objects.last()
            if not last_cycle:
                logging.debug('No Previous LendStats entry found.')
            time_since_last = timezone.now() - last_cycle.created_at
            if time_since_last < datetime.timedelta(seconds=9):
                logging.warning('Save fired too quickly since last save. Time since last save {}'.found(
                    time_since_last.seconds))
                time.sleep(freqency)
                continue
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
            logging.info('Completed: {} loop at price: {}'.format(x, avg_low_bid))
        time.sleep(freqency)


save_lending_stats()

import logging
from django.utils import timezone
import datetime
import decimal
import time
import rainmaker.models
from poloapi.restapi import poloniex
freqency = 10  # seconds
seconds_in_hour = 60 * 60
num_loops = (seconds_in_hour / freqency)


def save_lending_stats():
    freqency = 10  # seconds
    seconds_in_hour = 60 * 60
    num_loops = (seconds_in_hour / freqency)
    for x in xrange(num_loops):
        last_cycle = rainmaker.models.LendStats.objects.last()
        if not last_cycle:
            logging.debug('No Previous LendStats entry found.')
        time_since_last = time.timezone.now() - last_cycle.created_at
        if time_since_last < datetime.timedelta(seconds=9):
            logging.warning('Save fired too quickly since last save. Time since last save {}'.format(
                time_since_last.seconds))
            time.sleep(.5)
        p = poloniex()
        objects_list = []
        bid_asks = []
        loans = p.returnLoanOrders('BTC')['offers']
        i = 0
        for loan in loans:
            i += 1
            percent = decimal.Decimal(loan['rate']) * 100
            amount = BitcoinDecimal(loan['amount'])
            objects_list.append(rainmaker.models.LendHistory(amount=amount,
                                                      interest_ask=percent))
            if i > 25:
                bid_asks.append(percent)
        rainmaker.models.LendHistory.objects.bulk_create(objects_list)
        avg_low_bid = sum(bid_asks) / len(bid_asks)
        rainmaker.models.LendStats.objects.create(avg_interest_ask=avg_low_bid)
        logging.info('Save completed at price: {}'.format(avg_low_bid))
        print 'Save completed at price: {}'.format(avg_low_bid)
        return
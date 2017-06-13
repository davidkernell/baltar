import datetime
import decimal
import logging
import time

import django.core.management
from django.utils import timezone

import rainmaker.models
from poloapi.restapi import poloniex


class Command(django.core.management.BaseCommand):
    def handle(self, *args, **options):
        task_start_time = timezone.now()
        loop_start_time = None
        freqency = 10  # seconds
        seconds_in_hour = 60 * 60
        num_loops = (seconds_in_hour / freqency)
        for x in xrange(num_loops):
            if loop_start_time:
                time_since_last = timezone.now() - loop_start_time
                while time_since_last < datetime.timedelta(seconds=freqency):
                    logging.warning('Save fired too quickly since last save. Time since last save {}'.format(
                        time_since_last.seconds))
                    time.sleep(.5)
                    time_since_last = timezone.now() - loop_start_time
            p = poloniex()
            objects_list = []
            bid_asks = []
            loans = p.returnLoanOrders('BTC')['offers']
            i = 0
            for loan in loans:
                i += 1
                percent = decimal.Decimal(loan['rate']) * 100
                amount = decimal.Decimal(loan['amount'])
                objects_list.append(rainmaker.models.LendHistory(amount=amount,
                                                                 interest_ask=percent))
                if i > 25:
                    bid_asks.append(percent)
            rainmaker.models.LendHistory.objects.bulk_create(objects_list)
            avg_low_bid = sum(bid_asks) / len(bid_asks)
            rainmaker.models.LendStats.objects.create(avg_interest_ask=avg_low_bid)
            logging.info('Save completed at price: {}'.format(avg_low_bid))
            print 'Save completed at price: {}'.format(avg_low_bid)
            time_since_start = timezone.now() - task_start_time
            if time_since_start > datetime.timedelta(hours=1):
                logging.info(
                    'Save Lending stats Task started at {} and ended at {} UTC'.format(task_start_time.isoformat(),
                                                                                       timezone.now()))
                return
            loop_start_time = timezone.now()
            time.sleep(freqency)

# segmented_rates = range(0, 1001)
# segmented_rates_percent = [utils.BitcoinDecimal(rate)/1000 for rate in segmented_rates]
# segmented_rates_dict = dict((rate_band, 0) for rate_band in segmented_rates_percent)
import datetime
import time

import decimal

import django.db.transaction
from django.utils import timezone
import poloapi.restapi
import rainmaker.models
import rainmaker.utils


def log_loan_rate():
    bid_asks = []
    p = poloapi.restapi.poloniex()
    loans = p.returnLoanOrders('BTC')['offers']
    print len(loans)
    for loan in loans[:25]:
        percent = decimal.Decimal(loan['rate']) * 100
        # floor_percent = floor.quantize(utils.BitcoinDecimal('.001'))
        bid_asks.append(percent)
        # segmented_rates_dict[floor_percent] += utils.BitcoinDecimal(loan['rate'])
    avg_low_bid = sum(bid_asks) / len(bid_asks)
    return avg_low_bid


@django.db.transaction.atomic
def save_lending_stats():
    time.sleep(10)
    last_cycle = rainmaker.models.LendStats.objects.last()
    if last_cycle and last_cycle.created_at + datetime.timedelta(seconds=8) > timezone.now():
        print 'too early'
        return
    p = poloapi.restapi.poloniex()
    objects_list = []
    bid_asks = []
    loans = p.returnLoanOrders('BTC')['offers']
    i = 0
    for loan in loans:
        i += 1
        percent = decimal.Decimal(loan['rate']) * 100
        amount = rainmaker.utils.BitcoinDecimal(loan['amount'])
        objects_list.append(rainmaker.models.LendHistory(amount=amount,
                                                         interest_ask=percent))
        if i > 25:
            bid_asks.append(percent)
    rainmaker.models.LendHistory.objects.bulk_create(objects_list)
    avg_low_bid = sum(bid_asks) / len(bid_asks)
    rainmaker.models.LendStats.objects.create(avg_interest_ask=avg_low_bid)

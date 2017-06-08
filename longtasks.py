import os

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


@atomic
def save_lending_stats():
    print 'CALLED DB STATS FUNCTION'
    last_cycle = LendStats.objects.last()
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
        amount = BitcoinDecimal(loan['amount'])
        objects_list.append(LendHistory(amount=amount,
                                        interest_ask=percent))
        if i > 25:
            bid_asks.append(percent)
    LendHistory.objects.bulk_create(objects_list)
    avg_low_bid = sum(bid_asks) / len(bid_asks)
    LendStats.objects.create(avg_interest_ask=avg_low_bid)
    print 'cycle completed', LendStats.objects.last().avg_interest_ask
    time.sleep(10)

save_lending_stats()
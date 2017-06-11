import logging
import os

import msafescraper.utils

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
import time
import datetime
from django.utils import timezone
import decimal
import json

import requests
from twilio.rest import Client
import poloapi.restapi
from rainmaker.models import LendHistory, LendStats
from rainmaker.utils import BitcoinDecimal
from msafescraper.models import FormPost

try:
    from django.conf import settings
except:
    import settings

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
            time.sleep(.5)
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
        return


def check_for_safe_dev_post():
    FORM_URL = 'http://forum.safedev.org/'
    DEV_ACCT_ID = 205

    known_posts = FormPost.objects.values_list('topic_id', flat=True)
    page = requests.get(FORM_URL)
    start_str = 'ps.store("topic_list_latest"'
    end_str = '}]}]}});\n'
    data_start = page.content.find(start_str) + len(start_str) + 2
    data_end = page.content.find(end_str, data_start) + len(end_str) - 3
    print page.content
    post_data = json.loads(page.content[data_start:data_end])
    for topic in post_data['topic_list']['topics']:
        if topic['id'] in known_posts:
            continue
        for posters in topic['posters']:
            if posters[u'description'] == u'Original Poster':
                FormPost.objects.create(topic_id=topic['id'],
                                        dev_blog=True if posters['user_id'] == DEV_ACCT_ID else False)
                if posters['user_id'] == DEV_ACCT_ID:
                    client = Client(getattr(settings, 'ACCOUNT_SID', None), getattr(settings, 'AUTH_TOKEN', None))

                    message = client.messages.create(
                        to=getattr(settings, 'ADMIN_PHONE', None),
                        from_=getattr(settings, 'TWILIO_PHONE', None),
                        body="NEW MAIDSAFE DEV POST!!!!!!")
                    print(message.sid)
    print 'check posts'


def run_scripts():
    save_lending_stats()
    check_for_safe_dev_post()
    time.sleep(10)

if __name__ == '__main__':
    while 1 > 0:
        run_scripts()

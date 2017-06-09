import json

import msafescraper.models
import requests
from lxml import html
from twilio.rest import Client
from django.conf import settings

FORM_URL = 'http://forum.safedev.org/'
DEV_ACCT_ID = 205


def check_for_dev_post():
    known_posts = msafescraper.models.FormPost.objects.values_list('topic_id', flat=True)
    page = requests.get(FORM_URL)
    start_str = 'ps.store("topic_list_latest"'
    end_str = '}]}]}});\n'
    data_start = page.content.find(start_str) + len(start_str) + 2
    data_end = page.content.find(end_str, data_start) + len(end_str) - 3
    post_data = json.loads(page.content[data_start:data_end])
    for topic in post_data['topic_list']['topics']:
        if topic['id'] in known_posts:
            continue
        for posters in topic['posters']:
            if posters[u'description'] == u'Original Poster':
                msafescraper.models.FormPost.objects.create(topic_id=topic['id'],
                                                            dev_blog=True if posters['user_id'] == DEV_ACCT_ID else False)
                if posters['user_id'] == DEV_ACCT_ID:
                    client = Client(getattr(settings, 'ACCOUNT_SID', None), getattr(settings, 'AUTH_TOKEN', None))

                    message = client.messages.create(
                        to=getattr(settings, 'ADMIN_PHONE', None),
                        from_=getattr(settings, 'TWILIO_PHONE', None),
                        body="NEW MAIDSAFE DEV POST!!!!!!")

                    print(message.sid)

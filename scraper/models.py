from __future__ import unicode_literals

from django.db import models


class MaidSafeFormPost(models.Model):
    topic_id = models.SmallIntegerField()
    dev_blog = models.BooleanField(default=False)
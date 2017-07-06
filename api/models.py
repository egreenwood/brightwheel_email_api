from __future__ import unicode_literals

from django.db import models


class EmailRequest(models.Model):
    to = models.CharField(max_length=200, blank=False)
    to_name = models.CharField(max_length=200, blank=False)
    sender = models.CharField(db_column='from', max_length=200, blank=False)
    from_name = models.CharField(max_length=200, blank=False)
    subject = models.CharField(max_length=200, blank=False)
    body = models.CharField(max_length=200, blank=False)
    errors = models.CharField(max_length=200, null=True, blank=True)

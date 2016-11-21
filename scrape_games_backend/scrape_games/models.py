from __future__ import unicode_literals

from django.db import models


class MyCacheTable(models.Model):
    cache_key = models.CharField(primary_key=True, max_length=255)
    value = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        db_table = 'my_cache_table'

class HitCount(models.Model):
    hits = models.IntegerField()

class ProgressBar(models.Model):
    session_id = models.TextField(primary_key=True)
    progress_bar = models.FloatField()
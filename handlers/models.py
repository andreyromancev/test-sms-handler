from django.db import models
from django.contrib.postgres.fields import JSONField


class RequestLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=256)
    request_data = JSONField(null=True)
    phone = models.CharField(max_length=32, null=True)


class RequestLogError(models.Model):
    log = models.OneToOneField('RequestLog', related_name='error')
    code = models.IntegerField(null=True)
    message = models.TextField(null=True)

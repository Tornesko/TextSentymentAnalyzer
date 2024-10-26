from django.db import models


class Text(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    sentiment_textblob = models.FloatField(default=0.0)
    sentiment_vader = models.FloatField(default=0.0)
    sentiment_transformer = models.FloatField(default=0.0)

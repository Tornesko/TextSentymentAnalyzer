from django.db import models


class Text(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    sentiment_score = models.FloatField(null=True, blank=True)

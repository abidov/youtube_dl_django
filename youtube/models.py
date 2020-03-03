from django.db import models

class YoutubeModel(models.Model):
    url = models.URLField(unique=True)
    mp3_title = models.CharField(max_length=255)
    mp3_id = models.CharField(max_length=255, unique=True)

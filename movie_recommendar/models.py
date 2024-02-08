from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length = 255)
    poster_url = models.URLField()

    def __str__(self):
        return self.title

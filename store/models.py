from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster_link = models.URLField()
    released_year = models.IntegerField()
    certificate = models.CharField(max_length=10, blank=True, null=True)
    runtime = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    imdb_rating = models.FloatField()
    overview = models.TextField()
    meta_score = models.IntegerField(blank=True, null=True)
    director = models.CharField(max_length=100)
    stars = models.CharField(max_length=255)
    votes = models.IntegerField()
    gross = models.CharField(max_length=50)
    is_rented = models.BooleanField(default=False)  # For rent button

    def __str__(self):
        return self.title

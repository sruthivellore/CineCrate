
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=254) 
    def __str__(self):
        return self.user.username


class Rented(models.Model):
    movie_id = models.CharField(max_length=200, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    charges = models.FloatField()

    def __str__(self):
        return f"{self.user.username} rented movie with ID {self.movie_id} on {self.start_date}"

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse





class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='movie/images/')
    category = models.CharField(max_length=250)
    year = models.IntegerField(default=2000)
    release_date = models.DateTimeField(blank=True, null=True)
    actors=models.CharField(max_length=250)
    url = models.URLField(blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'


class Review(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_again = models.BooleanField()


    def __str__(self):
        return self.text[:40]

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        db_table = 'review'

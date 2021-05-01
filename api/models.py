from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=50)
    idd = models.CharField(max_length=50, unique=True)
    age = models.IntegerField()
    self_url = models.CharField(max_length=100)
    albums_url = models.CharField(max_length=100)
    tracks_url = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=50)
    gen = models.CharField(max_length=50)
    idd = models.CharField(max_length=50, unique=True)
    artist_id = models.ForeignKey(Artist, to_field='idd', on_delete=models.CASCADE)
    artist_url = models.CharField(max_length=100)
    self_url = models.CharField(max_length=100)
    tracks_url = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=50)
    duration = models.FloatField()
    times_played = models.IntegerField()
    idd = models.CharField(max_length=50)
    album_id = models.ForeignKey(Album, to_field='idd', on_delete=models.CASCADE)
    artist_id = models.CharField(max_length=50)
    self_url = models.CharField(max_length=100)
    artist_url = models.CharField(max_length=100)
    album_url = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.
class Album(models.Model):
    id = models.AutoField(primary_key=True)
    artist = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    released = models.IntegerField()
    description = models.TextField(max_length=200)

class Track(models.Model):
    id = models.AutoField(primary_key=True)
    track_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=50)
    album = models.ForeignKey(Album, blank=False, null=False, on_delete=models.CASCADE, related_name='tracks')



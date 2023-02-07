from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BoardGame(models.Model):
    name = models.CharField(max_length=100)
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

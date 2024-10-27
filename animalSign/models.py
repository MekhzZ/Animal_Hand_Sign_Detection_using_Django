from django.db import models

# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    introduction = models.TextField()

    def __str__(self):
        return self.name

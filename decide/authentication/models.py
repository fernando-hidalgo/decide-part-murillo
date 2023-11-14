from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return self.username

    def save(self):
        self.save()

    def clean(self):
        pass

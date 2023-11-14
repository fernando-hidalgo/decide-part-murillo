from django.db import models
from django.contrib.auth.password_validation import validate_password


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, blank=False)
    password = models.CharField(
        max_length=100, blank=False, validators=[validate_password]
    )
    email = models.EmailField(unique=True, blank=False)

    def __str__(self):
        return self.username

    def save(self):
        self.save()

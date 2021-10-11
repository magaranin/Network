from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    description = models.CharField(max_length = 2000)

    def __str__(self):
        return f"{self.id}: {self.description}"
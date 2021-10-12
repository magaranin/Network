from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null= True, related_name="owner")
    description = models.CharField(max_length = 2000)
    like = models.IntegerField(default=0)

    def __str__(self):
        return {
            "id": self.id,
            "owner": self.username,
            "description": self.description,
            "created_date": self.created_date.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like
        }
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followed_users = models.ManyToManyField("self", symmetrical=False, related_name="follower_set")
    followers = models.ManyToManyField("self", symmetrical=False, related_name="followed_user_set")

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null= True, related_name="owned_posts")
    description = models.CharField(max_length = 2000)
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.owner} added a post on {self.created_date}"

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")


    def __str__(self):
        return f"'{self.content}' posted by {self.owner} on {self.timestamp}"

class Follow(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")

    def __str__(self):
        return f"'{self.user1}' is following {self.user2}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"'{self.user}' liked {self.post}"
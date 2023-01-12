from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"

class Bids(models.Model):
    bid = models.IntegerField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")

    def __str__(self):
        return f"{self.bid}"

class Auctions(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=640)
    initial_bid = models.ForeignKey(Bids, on_delete=models.CASCADE, blank=True, null=True, related_name="bids" )
    image_url = models.CharField(max_length=6400)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User,blank=True, null=True, related_name="user_watchlist")

    def __str__(self):
        return f"{self.owner} is selling a/an {self.title} for a starting price of {self.initial_bid}"


class Comment(models.Model):
    commenter =  models.ForeignKey(User,  on_delete=models.CASCADE, blank=True, null=True, related_name="commenter")
    auction_commented =  models.ForeignKey(Auctions,  on_delete=models.CASCADE, blank=True, null=True, related_name="auction_commented")
    comment = models.CharField(max_length=640)

    def __str__(self):
        return f"{self.commenter} made a comment on {self.auction_commented}."

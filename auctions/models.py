from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    name = models.CharField(max_length=40)
    discription = models.CharField(max_length=300)
    category = models.CharField(max_length=40)
    price = models.FloatField()
    create_date = models.DateField()
    create_time = models.TimeField()
    img_url = models.URLField()
    watching_users = models.ManyToManyField(User,blank=True,related_name="watchlist")
    creator = models.ForeignKey(User,default=1,on_delete=models.CASCADE,related_name="created_listings")
    closed = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.name}" 


class Bid(models.Model):
    product = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="bids")
    current_price = models.FloatField()
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bids")

    def __str__(self):
        return f"The bid was by {self.name} on {self.product.name} of ${self.current_price}"


class Comment(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commented")
    product = models.ForeignKey(AuctionListing,on_delete=models.CASCADE,related_name="comments")
    comment = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.person} on {self.product}:{self.comment}"
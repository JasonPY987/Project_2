from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import render


class User(AbstractUser):
    pass

class catagory(models.Model):
    NameCatagory = models.CharField(max_length=50)
    
    def __str__(self):
        return self.NameCatagory
    

class Listing(models.Model):
    ProductName = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    imageURL = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isActive = models.BooleanField(default= True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    catagory = models.ForeignKey(catagory, on_delete=models.CASCADE, blank=True, related_name="catagory")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")
    
    def __str__(self):
        return self.ProductName
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="userComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="listingComment")
    message = models.CharField(max_length=300)
    
    def __str__(self):
        return f"{self.author} comment on {self.listing}"

    
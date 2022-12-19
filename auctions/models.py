from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class catagory(models.Model):
    NameCatagory = models.CharField(max_length=50)
    
    def __str__(self):
        return self.NameCatagory
    

class Listing(models.Model):
    ProductName = models.CharField(max_length=50)
    date = models.DateField()
    description = models.CharField(max_length=300)
    imageURL = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isActive = models.BooleanField(default= True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    catagory = models.ForeignKey(catagory, on_delete=models.CASCADE, blank=True, related_name="catagory")
    
    def __str__(self):
        return self.ProductName
    
def ListingCreate(request):
    if request.method == "GET":
        return render(request, "auctions/create.html")
    
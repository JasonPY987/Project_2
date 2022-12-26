from django.contrib import admin
from .models import Listing, User, catagory, Comment, Bid



# Register your models here.
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(catagory)
admin.site.register(Comment)
admin.site.register(Bid)
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.ListingCreate, name="create"),
    path("DisplayCategory", views.DisplayCategory, name="DisplayCategory"),
    path("cart", views.cart, name="cart"), 
    path("listing/<int:id>", views.listing, name="listing"),
    path("removeWatchList/<int:id>", views.removeWatchList, name="removeWatchList"),
    path("addWatchList/<int:id>", views.addWatchList, name="addWatchList"),
    path("Display_Watch_List", views.Display_Watch_List, name="Display_Watch_List"),
    path("newComment/<int:id>", views.newComment, name="newComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction"),
]

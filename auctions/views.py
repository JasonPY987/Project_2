from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from .models import User, catagory, Listing, Comment

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    listinginwatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "listinginwatchlist": listinginwatchlist,
        "allComments": allComments
    })
    
def newComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment']
    
    addComment = Comment (
        author = currentUser,
        listing = listingData,
        message = message
    )
    
    addComment.save()
    
    return HttpResponseRedirect(reverse("listing", args=(id,)))
    
def Display_Watch_List(request):
    currentUser = request.user
    listings = currentUser.listingwatchlist.all()
    return render(request, "auctions/Display_Watch_List.html", {
        "listings": listings
    })
    
def removeWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def addWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = catagory.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories,
    })
    
def DisplayCategory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['menu']
        category = catagory.objects.get(NameCatagory=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, catagory=category)
        allCategories = catagory.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories,
        })
    
 

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    
def ListingCreate(request):
    if request.method == "GET":
        allCategories = catagory.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["menu"]
        cuttentuser = request.user 
        categoryData = catagory.objects.get(NameCatagory=category)
        newListing = Listing(
            ProductName=title,
            description = description,
            imageURL = imageurl,
            price = float(price),
            catagory = categoryData,
            owner = cuttentuser
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
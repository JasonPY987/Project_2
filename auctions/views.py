from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from .models import User, catagory, Listing, Comment, Bid

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    listinginwatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    Good_Owner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "listinginwatchlist": listinginwatchlist,
        "allComments": allComments,
        "Good_Owner": Good_Owner,
    })
    
def close_auction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    listinginwatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    Good_Owner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "listinginwatchlist": listinginwatchlist,
        "allComments": allComments,
        "Good_Owner": Good_Owner,
        "update": True, 
        "message": "Congradulations, you just got paid!! "
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
    listings = currentUser.listingWatchlist.all()
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
        bid = Bid(bid=int(price), user=cuttentuser)
        bid.save()
        newListing = Listing(
            ProductName=title,
            description = description,
            imageURL = imageurl,
            price = bid,
            catagory = categoryData,
            owner = cuttentuser
            
        )
        newListing.save()
        return HttpResponseRedirect(reverse(index))
    
def addBid(request,id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    listinginwatchlist = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    Good_Owner = request.user.username == listingData.owner.username
    if int(newBid) > listingData.price.bid:
        updateBid = Bid(user=request.user, bid=int(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "sucessful bid update",
            "update": True,
            "listinginwatchlist": listinginwatchlist,
            "allComments": allComments,
            "Good_Owner": Good_Owner,
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Failed bid update",
            "update": False,
            "listinginwatchlist": listinginwatchlist,
            "allComments": allComments,
            "Good_Owner": Good_Owner,
        })
        
def cart(request):
    listingData = Listing.objects.all
    orders = Listing.objects.filter(ProductName=request.ProductName)
    return render(request, "auctions/cart.html", {
        'orders': orders,
        'listingData': listingData 
    })
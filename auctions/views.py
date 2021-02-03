from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User,AuctionListing,Bid,Comment


def index(request):
    
    return render(request, "auctions/index.html",{
        "listings":AuctionListing.objects.all()
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


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        discription = request.POST["discription"]
        price = float(request.POST["price"])
        img_url = request.POST["img_url"]
        category = request.POST["category"]
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        creator = request.user
        if title is None or discription is None or price is None:
            return render(request,"auctions/create.html",{
                "msg":"Please Fill all the Fields first"
            })
        else:
            try:
                item = AuctionListing(name=title,discription=discription,category=category,price=price,create_date=current_date,create_time=current_time,img_url=img_url,creator=creator)
                item.save()
                initial_bid = Bid(product=item,current_price=price,name=request.user)
                initial_bid.save()
            except IntegrityError:
                return render(request,"auctions/create.html",{
                    "msg":"Something is wrong..!"
                })
            return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/create.html")


def listing(request,listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    latest_bid = listing.bids.all()[len(listing.bids.all())-1]
    total_num_bid = len(listing.bids.all())
    comments = listing.comments.all()
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "watching":listing in request.user.watchlist.all(),
        "latest_bid":latest_bid,
        "num_bids":total_num_bid,
        "comments":comments
    })

def watch(request,listing_id):
    listing = AuctionListing.objects.get(pk=int(listing_id))
    listing.watching_users.add(request.user)
    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

def watchlist(request):
    return render(request,"auctions/watchlist.html",{
        "listings":request.user.watchlist.all()
    })




def remove_watch(request,listing_id):
    listing = AuctionListing.objects.get(pk=int(listing_id))
    listing.watching_users.remove(request.user)
    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

def bid(request,listing_id):
    if request.method == "POST":
        product = AuctionListing.objects.get(pk=listing_id)
        bid_amount = float(request.POST["bid_amount"])
        if bid_amount <= product.bids.all()[len(product.bids.all())-1].current_price:
            return render(request,"auctions/error.html",{
                "msg":"Bid Amount should be greater than current bid amount."
            })
        
        name = request.user
        
        try:
            bid = Bid(name=name,current_price=bid_amount,product=product)
            bid.save()
        except IntegrityError:
            return HttpResponseRedirect(reverse("listing",args=(listing_id,)))
        return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

def bid_close(request,listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    listing.closed = True
    listing.save()
    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

def closed(request):
    return render(request, "auctions/closed.html",{
        "listings":AuctionListing.objects.all()
    })

def categories(request):
    return render(request,"auctions/categories.html")

def category(request,id):
    return render(request,"auctions/category.html",{
        "category":id,
        "listings":AuctionListing.objects.all()
    })

def comment(request,listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        person = request.user
        product = AuctionListing.objects.get(pk=listing_id)
        try:
            temp = Comment(comment=comment,person=person,product=product)
            temp.save()
        except IntegrityError:
            return render(request,"auctions/error.html",{
                "msg":"Your comment was not published"
            })
        return HttpResponseRedirect(reverse('listing',args=(listing_id,)))
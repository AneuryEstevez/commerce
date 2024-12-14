from ast import Try
from http.client import HTTPResponse
from logging import exception
from warnings import catch_warnings
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import DecimalField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.core.paginator import Paginator

from .models import Bid, Listing, User, Category, Comment
from .forms import *


def index(request):
    listings = Listing.objects.filter(isActive=True)
    paginator = Paginator(listings, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "auctions/index.html", {
        "listings": page_obj
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
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateUserForm()

    return render(request, "auctions/register.html", {"form": form})

@login_required
def createListing(request):
    if request.method == "POST":
        user = request.user
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
        
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all(),
        "form": form
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def categoryListings(request, category):
    try:
        # Category.objects.get(name=category):
        category = Category.objects.get(name=category)
    except ObjectDoesNotExist:
        return render(request, "auctions/index.html") 
    
    listings = Listing.objects.filter(isActive=True, category=category)
    paginator = Paginator(listings, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "auctions/index.html", {
        "category": category,
        "listings": page_obj
    })

def listingDetails(request, id):
    listing = get_object_or_404(Listing, id=id)
    user = request.user
    owner = False
    if user == listing.user:
        owner = True
    #Get the highest listing bid
    highestPrice = listing.bids.aggregate(price=Max('price'))
    if highestPrice["price"]:
        highestBid = listing.bids.get(price = highestPrice["price"])
    else:
        highestPrice["price"] = 0
        highestBid = None

    # if highestBid["price"] is None:
    #     highestBid["price"] = listing.price
    
    if request.method == "POST":
        price = float(request.POST["price"])

        if price > highestPrice["price"] and price > listing.price:
            bid = Bid(
                listing = listing,
                user = user,
                price = price
            )
            bid.save()
            highestBid = bid
            return render(request, "auctions/details.html", {
                "listing": listing,
                "owner": owner,
                "highestBid": highestBid,
                "comments": listing.comments.all(),
                "message": "Your bid was submitted!",
                "submitted": True
            })
        else:
            return render(request, "auctions/details.html", {
                "listing": listing,
                "owner": owner,
                "highestBid": highestBid,
                "comments": listing.comments.all(),
                "message": "Bid price is too low",
                "submitted": False
            })
    else:
        return render(request, "auctions/details.html", {
            "listing": listing,
            "owner": owner,
            "highestBid": highestBid,
            "comments": listing.comments.all()
        })

@login_required
def watchListing(request, id):
    user = request.user
    listing = Listing.objects.get(id=id)
    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)

    return HttpResponseRedirect(reverse('listings', args=[id]))

@login_required
def watchlist(request):
    user = request.user
    listings = user.watchlist.all()
    paginator = Paginator(listings, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "auctions/index.html", {
        "listings": page_obj
    })


@login_required
def comment(request, id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(id=id)
        message = request.POST["comment"]
        
        comment = Comment(
            user = user,
            listing = listing,
            message= message
        )
        comment.save()
        return HttpResponseRedirect(reverse('listings', args=[id]))

def closeAuction(request, id):
    listing = Listing.objects.get(id=id)
    owner = False
    if request.user == listing.user:
        owner = True
    #Get the highest listing bid
    highestPrice = listing.bids.aggregate(price=Max('price'))
    highestBid = listing.bids.get(price = highestPrice["price"])
    
    if request.method == "POST":
        listing.isActive = False
        listing.save()
        return render(request, "auctions/details.html", {
            "listing": listing,
            "owner": owner,
            "highestBid": highestBid,
            "comments": listing.comments.all(),
            "message": "The auction was closed",
            "submitted": True
        })

@login_required
def myListings(request):
    user = request.user
    listings = user.listings.all()
    paginator = Paginator(listings, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "auctions/listings.html", {
        "listings": page_obj
    })

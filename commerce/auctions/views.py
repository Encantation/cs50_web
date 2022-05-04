from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.db.models import Max
import datetime

from .models import User, Auction, Bids, Comments, Watchlists

class NewListingForm(forms.Form):
    title = forms.CharField(label='Entry listing name')
    description = forms.CharField(label='Entry description')
    start_bid = forms.FloatField(label='Starting bid')
    url_link = forms.CharField(label='Entry media URL')
    category = forms.CharField(label='Entry category')


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(state="Open")
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

def new_listing (request):
    form = NewListingForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            auc = Auction(title=form.cleaned_data["title"],
                          description=form.cleaned_data["description"],
                          seller=request.user,
                          price=form.cleaned_data["start_bid"],
                          url_link=form.cleaned_data["url_link"],
                          category=form.cleaned_data["category"],
                          post_date=datetime.datetime.now())
            auc.save()
        return render(request, "auctions/index.html", {
            "auctions": Auction.objects.all()
            })
    elif request.method == "GET":
        return render(request, "auctions/create_listing.html", {
        "new_listing_form": NewListingForm()
        })

def listing (request):
    if request.method == "POST":
        if 'close_auc' in request.POST:
            auction = Auction.objects.get(id=request.POST["auction_id"])
            auction.state = 'Closed'
            auction.save()
        if 'bid_value' in request.POST:
            new_bid = Bids(lot=Auction.objects.get(id=request.POST["auction_id"]),
                           bidder=User.objects.get(id=request.POST["user_id"]),
                           bid=request.POST["bid_value"])
            new_bid.save()
        if 'add_watch' in request.POST:
            watchlist = Watchlists(watcher=User.objects.get(id=request.POST["user_id"]),
                                   auction=Auction.objects.get(id=request.POST["auction_id"]))
            try:
                watchlist.save()
            except:
                return render(request, "auctions/listing.html", {
                    "auction": Auction.objects.get(id=request.GET["id"]),
                    "message": "Watch already exists!"
                })
        return render(request, "auctions/index.html", {
            "auctions": Auction.objects.filter(state="Open")
        })
    else:
        auction = Auction.objects.get(id=request.GET["id"])
        bids = Bids.objects.filter(lot=auction.id)
        if bids.count() == 0:
            max_bid = auction.price
        else:
            max_bid = bids.aggregate(Max('bid')).get('bid__max')
        return render(request, "auctions/listing.html", {
            "auction": auction,
            "bids": bids.count(),
            "max_bid": max_bid
        })

def watchlist(request):
    if 'rm_watch' in request.POST:
        Watchlists.objects.filter(id=request.POST["watchlist_id"]).delete()
    return render(request, "auctions/watchlist.html", {
        "watchlists": Watchlists.objects.select_related().filter(watcher=request.GET["user_id"])
    })
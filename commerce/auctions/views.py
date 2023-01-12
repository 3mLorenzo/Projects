from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Auctions, Category, Comment, Bids


def index(request):
    return render(request, "auctions/index.html",{
        "auctions":Auctions.objects.all(),
        "categories":Category.objects.all()
    })


def watchlist(request):
    user = request.user
    auctions = user.user_watchlist.all()

    return render(request, "auctions/watchlist.html",{
            "auctions":auctions
        })


def listing(request, id):
    auction = Auctions.objects.get(pk=id)
    in_watchlist = request.user in auction.watchlist.all()
    all_comments = Comment.objects.filter(auction_commented=auction)
    owner = request.user.username == auction.owner.username

    return render(request, "auctions/listing.html",{
        "auction":auction,
        "in_watchlist":in_watchlist,
        "all_comments":all_comments,
        "owner":owner
    })

def close(request, id):
    auction = Auctions.objects.get(pk=id)
    auction.active = False
    auction.save()
    in_watchlist = request.user in auction.watchlist.all()
    all_comments = Comment.objects.filter(auction_commented=auction)
    owner = request.user.username == auction.owner.username

    return render(request, "auctions/listing.html", {
            "auction":auction,
            "message":"Bid made succesfully!",
            "bid":0,
            "in_watchlist":in_watchlist,
            "all_comments":all_comments,
            "message":"Your Auction is closed!",
            "owner":owner
        })


def remove_watchlist(request, id):
    auction = Auctions.objects.get(pk=id)
    user = request.user
    auction.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def add_watchlist(request, id):
    auction = Auctions.objects.get(pk=id)
    user = request.user
    auction.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))



def category_filter(request):
    if request.method == 'POST':
        category = request.POST["categories"]

        real_category = Category.objects.get(category_name=category)
        all_auctions = Auctions.objects.filter(active=True, category=real_category)

        return render(request, "auctions/index.html",{
            "auctions":all_auctions,
            "categories":Category.objects.all()
        })
        
    return render(request, "auctions/index.html",{
        "auctions":Auctions.objects.all(),
        "categories":Category.objects.all()
    })


@login_required
def new_auction(request):

    if request.method == 'POST':
        title = request.POST["title"] 
        description = request.POST["description"]
        initial_bid = request.POST["initial_bid"]
        image_url = request.POST["image_url"]
        category = request.POST["categories"]
        owner = request.user

        bid = Bids(bid=initial_bid, bidder=owner)
        bid.save()

        real_category = Category.objects.get(category_name=category)

        f = Auctions(
            title=title,
            description=description,
            initial_bid=bid,
            image_url=image_url,
            category=real_category,
            owner=owner
        )

        f.save()

        return render(request, "auctions/index.html",{
            "auctions":Auctions.objects.all(),
            "categories":Category.objects.all()
        })

    return render(request, "auctions/new_auction.html",{
                "categories":Category.objects.all()
        })

def comment(request, id):
    user = request.user
    auction = Auctions.objects.get(pk=id)
    comment = request.POST["comment"]

    f = Comment (
        commenter=user,
        auction_commented=auction,
        comment=comment
    )

    f.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def bid(request, id):
    bid = request.POST["bid"]
    auction_bid = Auctions.objects.get(pk=id)
    in_watchlist = request.user in auction_bid.watchlist.all()
    all_comments = Comment.objects.filter(auction_commented=auction_bid)

    if int(bid) > auction_bid.initial_bid.bid:
        f = Bids(bidder=request.user, bid=int(bid))
        f.save()
        auction_bid.initial_bid = f
        auction_bid.save()
        return render(request, "auctions/listing.html", {
            "auction":auction_bid,
            "message":"Bid made succesfully!",
            "bid":1,
            "in_watchlist":in_watchlist,
            "all_comments":all_comments
        })
    
    else:
        return render(request, "auctions/listing.html", {
            "auction":auction_bid,
            "message":"Bid not made!",
            "bid":-1,
            "in_watchlist":in_watchlist,
            "all_comments":all_comments
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

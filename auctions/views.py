from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages


from .models import User, Listing, Category, Comment, Bid
from . import forms as fm


def index(request):

    listings = Listing.objects.filter(
        is_active=True).order_by('-created_at')

    paginator = Paginator(listings, per_page=12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "auctions/index.html", {
        "page_obj": page_obj,
    })


def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category_detail(request, name):
    selected_category = get_object_or_404(Category, name=name)
    listings = Listing.objects.filter(
        is_active=True,
        category=selected_category
    ).order_by('-created_at')

    paginator = Paginator(listings, per_page=12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "auctions/category-detail.html", {
            "page_obj": page_obj,
            "name": name
        }
    )


@login_required(login_url="auctions:login")
def personal(request):
    listings = Listing.objects.filter(
        author=request.user).order_by('-created_at')
    paginator = Paginator(listings, per_page=12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "auctions/index.html", {
        "page_obj": page_obj
    })


def listing(request, id):
    listing = get_object_or_404(Listing, pk=id)
    total_bids = listing.bids.count()
    last_bidder = listing.bids.order_by('-created_at').first()
    is_watching = listing.users.filter(pk=request.user.pk).exists()
    return render(
        request,
        "auctions/listing.html", {
            "listing": listing,
            "bid_form": fm.BidForm(),
            "comment_form": fm.CommentForm(),
            "total_bids": total_bids,
            "last_bidder": last_bidder.user.username if last_bidder else "No bids yet",
            "is_watching": is_watching,
        }
    )


@login_required(login_url="auctions:login")
def close(request, id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=id)
        bid = listing.bids.order_by('-price').first()
        winner = bid.user if bid else None

        if winner:
            listing.winner = winner
            messages.success(request, f"User {winner.username} has won")

        listing.is_active = False
        listing.save()

    return HttpResponseRedirect(
        reverse("auctions:listing", args=(id,))
    )


@login_required(login_url="auctions:login")
def watch(request, id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=id)

        if listing.users.filter(pk=request.user.pk).exists():
            listing.users.remove(request.user)
        else:
            listing.users.add(request.user)

    return HttpResponseRedirect(
        reverse("auctions:listing", args=(id,))
    )


@login_required(login_url="auctions:login")
def watchlist(request):
    listings = request.user.watchlist.all()

    listings = sorted(
        listings,
        key=lambda listing: listing.winner != request.user
    )

    paginator = Paginator(listings, per_page=12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "auctions/watchlist.html", {
        "page_obj": page_obj
    })


@login_required(login_url="auctions:login")
def bid(request, id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=id)
        form = fm.BidForm(request.POST)
        if form.is_valid() and listing.author != request.user:
            bid = Bid(
                user=request.user,
                listing=listing,
                **form.cleaned_data
            )

            if form.cleaned_data['price'] < listing.price:
                messages.warning(
                    request,
                    "Your bid must be greater than the current price."
                )
            else:
                bid.price = listing.price = form.cleaned_data['price']
                listing.users.add(request.user)

                bid.save()
                listing.save()

                messages.success(
                    request, "Your bid was updated successfully.")

        else:
            return render(
                request,
                "auctions/listing.html", {
                    "listing": listing,
                    "bid_form": form,
                    "comment_form": fm.CommentForm()
                }
            )

    return HttpResponseRedirect(
        reverse("auctions:listing", args=(id,))
    )


@login_required(login_url="auctions:login")
def comment(request, id):
    if request.method == 'POST':
        form = fm.CommentForm(request.POST)
        listing = get_object_or_404(Listing, pk=id)

        if form.is_valid():
            comment = Comment.objects.create(
                author=request.user,
                listing=listing,
                **form.cleaned_data
            )
    else:
        form = fm.CommentForm()

    return HttpResponseRedirect(
        reverse("auctions:listing", args=(id,))
    )


@login_required(login_url="auctions:login")
def create(request):
    if request.method == "POST":
        form = fm.CreateListingForm(request.POST)

        if form.is_valid():
            listing = Listing.objects.create(
                author=request.user, **form.cleaned_data)

            listing.users.add(request.user)

            return HttpResponseRedirect(
                reverse("auctions:listing", args=(listing.pk,))
            )
    else:
        form = fm.CreateListingForm()

    return render(
        request,
        "auctions/create.html", {
            "form": form
        }
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

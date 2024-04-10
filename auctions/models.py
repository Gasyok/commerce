from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='listings', blank=True, null=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='wins',
        blank=True,
        null=True
    )
    users = models.ManyToManyField(
        User,
        blank=True,
        null=True,
        related_name='watchlist'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='listings')

    def __str__(self):
        return f"{self.title}- {self.price} ({self.is_active})"


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='bids'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bid {self.listing} for {self.price}"


class Comment(models.Model):
    content = models.CharField(max_length=255)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.author} to {self.listing} at {self.created_at}"

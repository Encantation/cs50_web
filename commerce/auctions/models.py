from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    title = models.CharField(max_length=32)
    watchlist = models.CharField(max_length=128, default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    price = models.FloatField()
    category = models.CharField(max_length=32, blank=True)
    description = models.CharField(max_length=128)
    url_link = models.CharField(max_length=64, blank=True)
    post_date = models.DateTimeField()
    state_choices = [('Open', 'Open'), ('Closed', 'Closed')]
    state = models.CharField(
        max_length=6,
        choices=state_choices,
        default='Open',
    )

    def __str__(self):
        return f"Lot {self.title}, start price {self.price}"

class Bids(models.Model):
    lot = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bidding_lots")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bidder} placed {self.bid} on lot {self.lot}"

class Comments(models.Model):
    lot = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment_lots")
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posters")
    comment = models.CharField(max_length=256)

class Watchlists(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchers")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watched_auctions")
    class Meta:
        unique_together = ["watcher", "auction"]

    def __str__(self):
        return f"{self.watcher} watches {self.auction.title}"
from django.contrib import admin

from .models import User, Auction, Bids, Comments, Watchlists
# Register your models here.

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlists)
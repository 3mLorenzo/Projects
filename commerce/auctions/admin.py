from django.contrib import admin
from .models import User, Auctions, Category, Comment, Bids
# Register your models here.


admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bids)
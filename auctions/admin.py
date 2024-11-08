from django.contrib import admin
from .models import Bid, User, Category, Listing, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
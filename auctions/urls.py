from venv import create
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categoryListings, name="categoryListings"),
    path("listings/<int:id>", views.listingDetails, name="listings"),
    path("watchLinsting/<int:id>", views.watchListing, name="watchListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("close/<int:id>", views.closeAuction, name="close"),
    path("myListings", views.myListings, name="myListings"),
]
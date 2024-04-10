from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("close/<int:id>", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("listings/me", views.personal, name="personal"),
    path("categories", views.category, name="categories"),
    path("categories/<str:name>", views.category_detail, name="categories-detail"),
]

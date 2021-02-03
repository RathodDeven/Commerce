from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.create,name="create"),
    path("listing/<int:listing_id>",views.listing,name="listing"),
    path("watch/<int:listing_id>",views.watch,name="watch"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("remove_watch/<int:listing_id>",views.remove_watch,name="remove_watch"),
    path("bid/<int:listing_id>",views.bid,name="bid"),
    path("listing/<int:listing_id>/close",views.bid_close,name="bid_close"),
    path("closed",views.closed,name="closed"),
    path("categories",views.categories,name="categories"),
    path("category/<str:id>",views.category,name="category"),
    path("comment/<int:listing_id>",views.comment,name="comment")
]

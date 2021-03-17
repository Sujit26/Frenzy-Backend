# Third party stuff
from rest_framework.routers import DefaultRouter

# Frenzy stuff
from frenzy.restaurant.api import RestaurantAPI, PopularAPI
from frenzy.user.api import UserAPI, TransactionAPI, NumberOfUsersAPI, TopXUsersAPI

default_router = DefaultRouter(trailing_slash=False)
default_router.register("restaurants", RestaurantAPI, basename="restaurants")
default_router.register("most-popular", PopularAPI, basename="most-popular")
default_router.register("user", UserAPI, basename="user")
default_router.register("transaction", TransactionAPI, basename="transaction")
default_router.register(
    "number-of-users", NumberOfUsersAPI, basename="number-of-users")
default_router.register("top-x-user", TopXUsersAPI, basename="top-x-user")

urlpatterns = default_router.urls

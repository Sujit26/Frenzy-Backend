from django.contrib import admin
from frenzy.restaurant.models import (
    FoodItem,
    OpenningTime,
    Restaurant
)

# Register your models here.
admin.site.register(FoodItem)
admin.site.register(OpenningTime)
admin.site.register(Restaurant)

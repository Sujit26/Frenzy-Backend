from django.db import models
from datetime import datetime
# Create your models here.

WEEKDAYS = [
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
]


class Restaurant(models.Model):
    name = models.CharField(
        max_length=99,
        blank=False,
        null=False,
        help_text="Restaurants name",
    )
    cash_balance = models.FloatField()

    def __str__(self):
        return f'{self.name}-{self.cash_balance}'


class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name}-{self.restaurant.name}'


class OpenningTime(models.Model):
    weekday = models.IntegerField(choices=WEEKDAYS, unique=True)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.restaurant.name}-{self.weekday}'


def dishes_in_range(restaurant: Restaurant, nod, min_price, max_price, mode):
    items = FoodItem.objects.filter(restaurant=restaurant).all()
    count_in_range = sum([
        1 for i in items if min_price <= i.price and i.price <= max_price])

    if mode == 'lte':
        return count_in_range <= nod
    else:
        return count_in_range >= nod

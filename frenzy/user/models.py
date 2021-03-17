from django.db import models
from frenzy.restaurant.models import Restaurant, FoodItem


class User(models.Model):
    name = models.CharField(
        max_length=99,
        blank=False,
        null=False,
        help_text="User name",
    )
    cash_balance = models.FloatField()

    def __str__(self):
        return f'{self.name}-{self.cash_balance}'


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    dish_name = models.ForeignKey(
        FoodItem,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    transaction_amount = models.FloatField()
    transaction_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user.name}-{self.restaurant.name}-{self.dish_name}'

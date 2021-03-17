from rest_framework import filters as drf_filters
from django_filters.fields import CSVWidget
from django_filters import rest_framework as df_filters
from frenzy.restaurant import models
from django.forms.fields import MultipleChoiceField
from datetime import datetime


class RestaurantFilter(df_filters.FilterSet):
    name = df_filters.CharFilter(label='Search', lookup_expr='icontains')
    time = df_filters.CharFilter(
        label='Open Restaurants', method='open_restaurants')
    hours_per_week_gte = df_filters.NumberFilter(
        label='Number of hours per week greater than equal',
        method='number_of_hours'
    )
    hours_per_week_lte = df_filters.NumberFilter(
        label='Number of hours per week less than equal',
        method='number_of_hours'
    )
    hours_per_day_gte = df_filters.NumberFilter(
        label='Number of hours per day greater than equal',
        method='number_of_hours'
    )
    hours_per_day_lte = df_filters.NumberFilter(
        label='Number of hours per day less than equal',
        method='number_of_hours'
    )

    def number_of_hours(self, queryset, value, *args, **kwargs):
        try:
            if args:
                noh = int(args[0])
                now = datetime.today()
                interval = value.split('_')[-2]
                mode = value.split('_')[-1]

                restaurants = queryset.all()
                open_res_ids = [
                    res.id
                    for res in restaurants
                    if self.is_open_for_x_hour(res, noh, interval, mode)
                ]
                queryset = queryset.filter(id__in=open_res_ids)
        except ValueError:
            pass
        return queryset

    def open_restaurants(self, queryset, value, *args, **kwargs):
        try:
            if args:
                time = int(args[0])
                time = datetime.utcfromtimestamp(time)

                opts = models.OpenningTime.objects.filter(
                    weekday=time.weekday())
                open_restaurants_ids = [
                    opt.restaurant.id for opt in opts
                    if time.time() >= opt.from_hour and time.time() <= opt.to_hour
                ]
                queryset = queryset.filter(id__in=open_restaurants_ids)
        except ValueError:
            pass
        return queryset

    def is_open_for_x_hour(self, restaurant, noh, interval, mode):
        timings = models.OpenningTime.objects.filter(
            restaurant=restaurant).all()

        now = datetime.today()
        hours_each_day = [
            (datetime.combine(now, t.to_hour) -
                datetime.combine(now, t.from_hour)).total_seconds()
            for t in timings
        ]

        if interval == 'week':
            total_hours = sum(hours_each_day)
            if mode == 'lte':
                return total_hours <= noh*3600
            else:
                return total_hours >= noh*3600
        else:
            if mode == 'lte':
                return any([t <= noh*3600 for t in hours_each_day])
            else:
                return any([t >= noh*3600 for t in hours_each_day])

    class Meta:
        model = models.Restaurant
        fields = ['name']

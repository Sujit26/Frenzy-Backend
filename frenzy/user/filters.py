from rest_framework import filters as drf_filters
from django_filters.fields import CSVWidget
from django_filters import rest_framework as df_filters
from frenzy.user import models
from django.forms.fields import MultipleChoiceField


class UserFilter(df_filters.FilterSet):
    class Meta:
        model = models.User
        fields = []

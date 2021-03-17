from django.contrib import admin

from frenzy.user.models import User, Transaction

# Register your models here.
admin.site.register(User)
admin.site.register(Transaction)

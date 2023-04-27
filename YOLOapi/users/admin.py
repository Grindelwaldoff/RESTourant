from django.contrib import admin

from .models import Business, Waiter, User

admin.site.register(User)
admin.site.register(Business)
admin.site.register(Waiter)
from django.contrib import admin

from .models import Dishes, Categories, Tables, QRCodes


admin.site.register(Dishes)
admin.site.register(Categories)
admin.site.register(Tables)
admin.site.register(QRCodes)



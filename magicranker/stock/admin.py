from django.contrib import admin

from magicranker.stock import models

admin.site.register(models.Detail)
admin.site.register(models.PerShare)
admin.site.register(models.BalSheet)
admin.site.register(models.PriceHistory)

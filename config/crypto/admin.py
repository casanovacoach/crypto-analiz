from django.contrib import admin
from .models import Snapshot, CoinPrice
# Register your models here.

admin.site.register(Snapshot)
admin.site.register(CoinPrice)
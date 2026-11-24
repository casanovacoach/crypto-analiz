from django.contrib import admin
from .models import Snapshot, CoinPrice
# Register your models here.

@admin.register(CoinPrice)
class CoinPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin_id', 'coin_name', 'price', 'snapshot_id')

class CoinPriceInline(admin.TabularInline):
    model = CoinPrice

@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ('snapshot_id', 'created_at')
    inlines = [CoinPriceInline]
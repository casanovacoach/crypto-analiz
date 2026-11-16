from django.db import models

# Create your models here.

class Snapshot(models.Model):
    snapshot_id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'snapshots'

class CoinPrice(models.Model):
    id = models.BigAutoField(primary_key=True)
    snapshot = models.ForeignKey(Snapshot, on_delete=models.CASCADE)
    coin_id = models.CharField(max_length=200)
    coin_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=40, decimal_places=20)

    class Meta:
        db_table = 'coin_prices'
        constraints = [
            models.UniqueConstraint(
                fields=['snapshot', 'coin_id'],
                name='unique_snapshot_coin'
            )
        ]
from rest_framework import serializers

from .models import CoinPrice, Snapshot

class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPrice
        fields = ('coin_id', 'coin_name', 'symbol', 'price')


class SnapshotSerializer(serializers.ModelSerializer):
    prices = CryptoSerializer(
        source='coinprice_set',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Snapshot
        fields = ('snapshot_id', 'created_at', 'prices')


class CoinHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPrice
        fields = ('snapshot', 'coin_id', 'coin_name', 'symbol', 'price')

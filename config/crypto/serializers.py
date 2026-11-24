from rest_framework import serializers

from .models import CoinPrice


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPrice
        fields = ('snapshot', 'coin_id')
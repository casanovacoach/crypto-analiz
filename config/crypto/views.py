from django.http import HttpResponse
from rest_framework.views import APIView, Response
from .serializers import CryptoSerializer

from crypto.models import CoinPrice


# Create your views here.

def index(request):
    return HttpResponse('Страница представления crypto')

def crypto(request):
    return HttpResponse('i m talk about crypto')

def snapshots(request, snap_id):
    return HttpResponse(f"<h1>Снимки</h1><p>id: {snap_id}</p>")


class CoinAPIView(APIView):
    def get(self, request, snap_id):
        coins = CoinPrice.objects.filter(snapshot_id = snap_id)
        serializer = CryptoSerializer(coins, many=True)
        return Response({'Coins' : serializer.data})
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView

from .serializers import CryptoSerializer, SnapshotSerializer, CoinHistorySerializer

from rest_framework.response import Response

from rest_framework.mixins import ListModelMixin

from .pagination import SnapshotPagination
from crypto.models import CoinPrice, Snapshot


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


class SnapshotViewSet(ModelViewSet):
    queryset = Snapshot.objects.order_by('snapshot_id')
    serializer_class = SnapshotSerializer
    pagination_class = SnapshotPagination
    http_method_names = ['get', 'head', 'options']


class CoinHistoryViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CoinHistorySerializer

    def get_queryset(self):
        coins = CoinPrice.objects.order_by('snapshot_id', 'id')
        symbol = self.request.query_params.get('symbol')

        if symbol:
            coins = coins.filter(symbol__iexact=symbol)

        return coins
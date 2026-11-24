from django.urls import path
from . import views

urlpatterns = [
    path('', views.crypto),
    path('snapshots/<int:snap_id>/', views.snapshots),
    path('api/snapshots/<int:snap_id>/', views.CoinAPIView.as_view()),
]
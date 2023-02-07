from django.urls import path
from .views import PublisherList, PublisherDetail, BoardGameList, BoardGameDetail, PublisherGamesList

urlpatterns = [
    path(r'publishers/', PublisherList.as_view()),
    path(r'publishers/<int:pk>/', PublisherDetail.as_view()),
    path(r'publishers/<int:pk>/board-games', PublisherGamesList.as_view()),
    path(r'board-games/', BoardGameList.as_view()),
    path(r'board-games/<int:pk>', BoardGameDetail.as_view())
]

from django.urls import path
from .views import json_news
from .views import news_main
from .views import NewsCreate

urlpatterns = [
    path('', news_main, name='news_main'),
    path('<int:news_id>/', json_news, name='json_news'),
    path('create/', NewsCreate.as_view(), name='news_create')
]
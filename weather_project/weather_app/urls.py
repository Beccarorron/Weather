from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('snow/', views.get_snow, name='snow'),
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pothole-picture/', views.pothole_picture, name='pothole-picture')
]
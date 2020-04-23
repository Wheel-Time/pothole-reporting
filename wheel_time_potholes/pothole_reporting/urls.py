from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views,forms

urlpatterns = [
    path('', views.index, name='index'),
    path('pothole-picture/', views.pothole_picture, name='pothole-picture'),
    path('pothole-geojson/', views.pothole_geojson, name='pothole-geojson'),
    url('login/', views.login_view, name='login'),
    url('signup/', views.signup_view, name='signup'),
]
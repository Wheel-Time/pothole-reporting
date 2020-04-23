from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views,forms

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/image', views.pothole_picture, name='pothole-picture'),
    path('pothole-geojson/', views.pothole_geojson, name='pothole-geojson'),
    url('login/', views.login_user, name='login'),
    url('signup/', views.create_user, name='signup'),
    path('submit/', views.submit_pothole, name='submit'),
    path('update/', views.update_pothole, name='update')
]
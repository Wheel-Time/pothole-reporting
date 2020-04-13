from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit/image', views.pothole_picture, name='pothole-picture'),
    path('pothole-geojson/', views.pothole_geojson, name='pothole-geojson'),
    path('submit/', views.submit_pothole, name='submit'),
    path('update/', views.update_pothole, name='update')
]
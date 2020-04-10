from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pothole-picture/', views.pothole_picture, name='pothole-picture'),
    path('pothole-geojson/', views.pothole_geojson, name='pothole-geojson'),
    path('submit/', views.submit_pothole, name='submit'),
    path('test-submit/', views.test_info_submission, name='test-submit')
]
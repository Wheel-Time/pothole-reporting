from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pothole-picture/', views.pothole_picture, name='pothole-picture'),
    path('pothole-geojson/', views.pothole_geojson, name='pothole-geojson'),
    path('ajax-test/', views.ajax_test, name='ajax-test'),
    path('add-pothole-ledger-entry/', views.add_pothole_ledger_entry, name='add-pothole-ledger-entry')
]
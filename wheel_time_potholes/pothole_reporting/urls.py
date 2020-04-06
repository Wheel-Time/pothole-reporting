from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views,forms

urlpatterns = [
    path('', views.index, name='index'),
    path('pothole-picture/', views.pothole_picture, name='pothole-picture'),
    path('pothole-geojson/', views.pothole_geojson, name='pothole-geojson'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='pothole_reporting/login.html',authentication_form=forms.login_form), name='login'),
    path('signup/', views.signup_view, name='signup'),
]
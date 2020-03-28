from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pothole-picture/', views.pothole_picture, name='pothole-picture'),
    path('login/', views.signup, name='signup'),
    path('login/signup/', views.newSignup, name='newSignup'),
]


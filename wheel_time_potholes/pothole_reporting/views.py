from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, 'pothole_reporting/index.html')


def pothole_picture(request):
    return render(request, 'pothole_reporting/pothole-picture.html')

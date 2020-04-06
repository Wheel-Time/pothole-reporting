from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from PIL import UnidentifiedImageError

from pothole_reporting.potholes.geotag_image import create_pothole_by_image
from pothole_reporting.potholes.geo_potholes import get_geojson_potholes
from .forms import (
    PotholeImageForm,
    login_form,
    signup_form)
from .exceptions import NoExifDataError


def index(request):
    return render(request,
                  'pothole_reporting/index.html',
                  {"api_key": settings.MAP_API_KEY})


def login_view(request):
    form = login_form(request.POST)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index') #redirect to the homepage for now
        else:
            messages.info(request,'username or password incorrect!')
    
    return render(request,"pothole_reporting/login.html")


def signup_view(request):
    form = signup_form(request.POST or None)
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account was created sucessfully for {username}!')
            return redirect('login')
        else:
            form = signup_form()
    return render(request,"pothole_reporting/signup.html", {'form':form})


def pothole_picture(request):
    text = ""

    if request.method == 'POST':
        form = PotholeImageForm(request.POST, request.FILES)
        if form.is_valid():

            image = request.FILES['file']
            try:
                create_pothole_by_image(image)
                # for now just redirect to same page - in future can send to confirmation page
                return HttpResponseRedirect(request.path_info)
            except UnidentifiedImageError:
                print("Unable to open image")
                text = "Unable to open the image"
            except (KeyError, NoExifDataError):
                print("Image had no geotag data")
                text = "Unable to get geo tag information from image. Make sure " \
                       "the image is a valid jpeg file with geo tag data."
        else:
            form = PotholeImageForm()

    else:  # GET request
        form = PotholeImageForm()

    return render(request,
                  'pothole_reporting/pothole-picture.html',
                  {'form': form,
                   'text': text})


def pothole_geojson(request):
    pothole_geojson = get_geojson_potholes(active=True)
    return HttpResponse(pothole_geojson)

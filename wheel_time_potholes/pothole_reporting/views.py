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
from .models import Pothole, PotholeLedger, SiteUser


def index(request):
    return render(request,
                  'pothole_reporting/index.html',
                  {"api_key": settings.MAP_API_KEY})


def login_view(request):
    form = login_form(request.POST)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = SiteUser.objects.filter(username=username, pword=password)
        if user.exists():
            return redirect('index')
        else:
            messages.info(request,'username or password incorrect!')

    return render(request,"pothole_reporting/login.html", {'form':form})


def signup_view(request):
    form = signup_form(request.POST or None)
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            print(password1)
            print(password2)
            if password1 == password2:
                user = SiteUser(username=username, first_name=first_name, last_name=last_name, email=email, pword=password1, is_admin=0)
                user.save()
                messages.success(request,f'Account was created sucessfully for {username}!')
                return redirect('login')
            else:
                messages.info(request, 'passwords do not match')
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

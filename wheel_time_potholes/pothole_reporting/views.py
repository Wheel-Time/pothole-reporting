from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from PIL import UnidentifiedImageError

from .forms import PotholeImageForm
from .geotag_image import create_pothole_by_image
from .exceptions import NoExifDataError


def index(request):
    return render(request,
                  'pothole_reporting/index.html',
                  {"api_key": settings.MAP_API_KEY})


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


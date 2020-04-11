from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.db import transaction, DatabaseError, IntegrityError
from django.utils import timezone
from PIL import UnidentifiedImageError

from pothole_reporting.potholes.geotag_image import create_pothole_by_image
from pothole_reporting.potholes.geo_potholes import get_geojson_potholes
from .forms import PotholeImageForm
from .models import Pothole, PotholeLedger
from .exceptions import NoExifDataError


def index(request):
    return render(request,
                  'pothole_reporting/index.html',
                  {"api_key": settings.MAP_API_KEY})


def submit_pothole(request):
    if request.method == 'GET':
        return render(request,
                      'pothole_reporting/submission.html',
                      {"api_key": settings.MAP_API_KEY})
    elif request.method == 'POST':
        req = request.POST
        current_datetime = timezone.now()

        pothole = Pothole(lat=req['lat'], lon=req['lon'], create_date=current_datetime)
        # TODO: Replace fk_user_id with SiteUser object that is attached to request
        p_ledger = PotholeLedger(fk_pothole=pothole, fk_user_id=1, state=req['state'], submit_date=current_datetime)

        try:
            with transaction.atomic():
                pothole.save()
                p_ledger.save()
        except (DatabaseError, IntegrityError):
            print("Transaction failed")

        return HttpResponse("SUCCESS")

def update_pothole(request):
    if request.method == 'GET':
        return render(request,
                      'pothole_reporting/submission.html',
                      {"api_key": settings.MAP_API_KEY})
    elif request.method == 'POST':
        req = request.POST
        current_datetime = timezone.now()

        pothole = Pothole.objects.get(id=request.POST['pothole_id'])
        # TODO: Replace fk_user_id with SiteUser object that is attached to request
        p_ledger = PotholeLedger(fk_pothole=pothole, fk_user_id=1, state=req['state'], submit_date=current_datetime)

        try:
            with transaction.atomic():
                pothole.save()
                p_ledger.save()
        except (DatabaseError, IntegrityError):
            print("Transaction failed")

        return HttpResponse("SUCCESS")

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
    pothole_geojson = get_geojson_potholes(active=False) # change back to true later
    return HttpResponse(pothole_geojson)


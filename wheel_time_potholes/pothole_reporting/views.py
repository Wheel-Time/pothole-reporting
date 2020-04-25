from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction, DatabaseError, IntegrityError
from django.utils import timezone
from PIL import UnidentifiedImageError

from pothole_reporting.potholes.geotag_image import create_pothole_by_image
from pothole_reporting.potholes.geo_potholes import get_geojson_potholes
from .forms import PotholeImageForm, LoginForm, SignupForm
from .models import Pothole, PotholeLedger
from .exceptions import NoExifDataError
from .models import Pothole, PotholeLedger, SiteUser


def _is_logged_in(request):
    return "user" in request.session


def index(request):
    return render(request,
                  'pothole_reporting/index.html',
                  {"api_key": settings.MAP_API_KEY,
                   "logged_in": _is_logged_in(request)})


def login_user(request):
    form = LoginForm(request.POST)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = SiteUser.objects.filter(username=username, pword=password)
        if user.exists():
            user = user[0]
            request.session['user'] = user.id
            request.session['logged_in'] = True
            return redirect('index')
        else:
            messages.info(request,'username or password incorrect!')

    return render(request,"pothole_reporting/login.html",
                  {'form':form,
                   "logged_in": _is_logged_in(request)})


def logout_user(request):
    if _is_logged_in(request):
        del request.session["user"]
        return HttpResponse("SUCCESS")
    else:
        return HttpResponse(status=400)


def create_user(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user = SiteUser(username=username, first_name=first_name, last_name=last_name, email=email, pword=password1, is_admin=0)
                user.save()
                messages.success(request,f'Account was created sucessfully for {username}!')
                return redirect('login')
            else:
                messages.info(request, 'passwords do not match')
    return render(request,"pothole_reporting/signup.html", {'form':form})


def submit_pothole(request):
    if request.method == 'GET':
        return render(request,
                      'pothole_reporting/submission.html',
                      {"api_key": settings.MAP_API_KEY,
                       "logged_in": _is_logged_in(request)})
    elif request.method == 'POST':
        if "user" in request.session:
            user_id = request.session["user"]
        else:
            return HttpResponse(status=401)

        req = request.POST
        current_datetime = timezone.now()

        pothole = Pothole(lat=req['lat'], lon=req['lon'], create_date=current_datetime)
        # TODO: Replace fk_user_id with SiteUser object that is attached to request
        p_ledger = PotholeLedger(fk_pothole=pothole, fk_user_id=user_id, state=req['state'], submit_date=current_datetime)

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
        if "user" in request.session:
            user_id = request.session["user"]
        else:
            return HttpResponse(status=401)

        req = request.POST
        current_datetime = timezone.now()

        pothole = Pothole.objects.get(id=request.POST['pothole_id'])
        # TODO: Replace fk_user_id with SiteUser object that is attached to request
        p_ledger = PotholeLedger(fk_pothole=pothole, fk_user_id=user_id, state=req['state'], submit_date=current_datetime)

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
    if request.method == 'GET':
        active = request.GET.get('active')
        active = (active is not None and active.lower() != "false")
        date = request.GET.get('date')
        pothole_geojson = get_geojson_potholes(active=active, date=date)
    return HttpResponse(pothole_geojson)


from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from PIL import UnidentifiedImageError

from .forms import PotholeImageForm
from .geotag_image import create_pothole_by_image
from .exceptions import NoExifDataError
from .models import SiteUser



def index(request):
    return render(request,
                  "pothole_reporting/index.html")

def signup(request):
    return render(request,
                  'signup_form/signup.html')

def newSignup(request):
    if request.method == "POST":
        userName = request.POST.get("username")
        fName = request.POST.get("first_name")
        lName = request.POST.get("last_name")
        eMail = request.POST.get("email")
        pWord = request.POST.get("pword")

        accepted_Admins = {"ipoulin@unomaha.edu","bishwokarki@unomaha.edu","emtriplett@unomaha.edu","fholzapfel@unomaha.edu"}

        is_Admin = False

        if eMail in accepted_Admins:
            is_Admin = True

        model_siteUser = SiteUser(username=userName,first_name=fName,last_name=lName,email=eMail,pword=pWord,is_admin=is_Admin)
        model_siteUser.save()
        return render(request,
                   'pothole_reporting/index.html') #redirect to the homepage for now

    else:
        return redirect('newSignup')
    

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


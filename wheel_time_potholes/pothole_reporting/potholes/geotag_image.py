from django.utils import timezone
from django.db import transaction, DatabaseError, IntegrityError
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from pothole_reporting.exceptions import NoExifDataError
from pothole_reporting.models import Pothole, PotholeLedger

# Much of this processing came from:
# https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3


def create_pothole_by_image(image, user_id, state):
    """
    create a new pothole using the geotagged data from an image
    return whether successful creation
    """
    coordinates = process_image(image)
    current_datetime = timezone.now()

    pothole = Pothole(lat=coordinates[0], lon=coordinates[1], create_date=current_datetime)
    p_ledger = PotholeLedger(fk_pothole=pothole, fk_user_id=user_id, state=state, submit_date=current_datetime)

    try:
        with transaction.atomic():
            pothole.save()
            p_ledger.save()
    except (DatabaseError, IntegrityError):
        print("Transaction failed")


def process_image(image):
    image = Image.open(image)
    image.verify()

    image_exif = image._getexif()
    if image_exif is None:
        raise NoExifDataError("image has no exif data")

    gps_data = get_gps_data(image_exif)
    coordinates = get_coordinates(gps_data)

    return coordinates


def get_gps_data(image_exif):
    gps_data = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in image_exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in image_exif[idx]:
                    gps_data[val] = image_exif[idx][key]

    return gps_data


def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat, lon)

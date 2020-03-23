from PIL import Image
from PIL.ExifTags import TAGS

from .exceptions import NoExifDataError


def create_pothole_by_image(image):
    """
    create a new pothole using the geotagged data from an image
    return whether successful creation
    """
    gps_data = process_image(image)
    print(gps_data)
    # TODO: once formatted, store as new pothole


def process_image(image):
    image = Image.open(image)
    image.verify()

    image_exif = image._getexif()
    if image_exif is None:
        raise NoExifDataError("image has no exif data")

    gps_data = label_data(image_exif)['GPSInfo']

    # TODO: format gps data properly for db
    return gps_data


def label_data(image_exif):
    labeled = {}
    for (key, val) in image_exif.items():
        labeled[TAGS.get(key)] = val

    return labeled

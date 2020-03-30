from geojson import Feature, Point, FeatureCollection, dumps
from datetime import datetime

from pothole_reporting.models import VwPothole


def convert_timestamp(ts):
    """
    convert MySQL timestamp to datetime
    """
    format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(ts, format)


def get_geojson_potholes(active=True):
    """
    If active is true, only return active potholes.
    If active is false, return all potholes.
    """

    potholes = VwPothole.objects.all()

    pothole_features = [Feature(
        geometry=Point((float(pothole.lon), float(pothole.lat)), precision=8),
        id=pothole.id,
        properties={"pothole_reports": int(pothole.pothole_reports),
                    "fixed_reports": int(pothole.fixed_reports),
                    "date": str(pothole.create_date)})
        for pothole in potholes
        # filter according to whether active is true
        if (active and convert_timestamp(pothole.fixed_date) > datetime.now())
        or not active]

    pothole_collection = FeatureCollection(pothole_features)
    return dumps(pothole_collection)

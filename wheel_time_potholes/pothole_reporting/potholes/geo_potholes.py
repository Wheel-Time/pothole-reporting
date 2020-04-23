from geojson import Feature, Point, FeatureCollection, dumps
from datetime import datetime

from pothole_reporting.models import VwPothole
from .pothole_queries import vw_pothole_by_date


def convert_timestamp(ts):
    """
    convert MySQL timestamp to datetime
    """
    format = '%Y-%m-%d %H:%M:%S'
    return datetime.strptime(ts, format)


def get_geojson_potholes(active=True, date=None):
    """
    If active is true, only return active potholes.
    If active is false, return all potholes.
    If date is set, then return potholes with ledger information
    up to the specified date
    date should be a string of the form: 'YYYY-MM-DD'
    """
    potholes = VwPothole.objects.all() if date is None \
        else VwPothole.objects.raw(vw_pothole_by_date, {'datetime': '{} 23:59:59'.format(date)})

    pothole_features = [Feature(
        geometry=Point((float(pothole.lon), float(pothole.lat)), precision=8),
        id=pothole.id,
        properties={"pothole_reports": int(pothole.pothole_reports),
                    "fixed_reports": int(pothole.fixed_reports),
                    "create_date": str(pothole.create_date),
                    "effective_date": str(pothole.effective_date),
                    "active": pothole.effective_date is not None
                                and convert_timestamp(pothole.effective_date) < datetime.utcnow()
                                and convert_timestamp(pothole.fixed_date) > datetime.utcnow(),
                    "fixed_date": str(pothole.fixed_date),
                    "fixed": pothole.fixed_date and convert_timestamp(pothole.fixed_date) < datetime.utcnow(),
                    "severity": str(('%f' % round(pothole.avg_severity, 2)).rstrip('.0')),
                    "utcnow": str(datetime.utcnow())
                    })
        for pothole in potholes
        # filter according to whether active is true
        if (active
            and pothole.effective_date is not None
            and convert_timestamp(pothole.fixed_date) > datetime.utcnow()
            and convert_timestamp(pothole.effective_date) < datetime.utcnow())
        or not active]

    pothole_collection = FeatureCollection(pothole_features)
    return dumps(pothole_collection)

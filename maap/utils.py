#from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.contrib.gis.geos import Polygon

from models import MaapZone, MaapArea


def import_areas(filepath, zone=True, categories= None):
    
    ds = DataSource(filepath)
    
    for e in ds[2]:
        pgeom = OGRGeometry(Polygon(e.geom.coords[0]).wkt)
        pgeom.srs = 'EPSG:4326'
        pgeom.transform_to(SpatialReference('EPSG:900913'))

        kwargs = dict( 
            geom = pgeom.wkt,
            name = e.get('name'),
            creator_id = 1,
            editor_id = 1,
        )
        if zone:
            ma = MaapZone(**kwargs)
        else:
            ma = MaapArea(**kwargs)

        ma.save()

        if categories:
            ma.category = categories
            ma.save()
        


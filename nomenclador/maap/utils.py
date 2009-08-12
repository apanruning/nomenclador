from django.contrib.gis.utils import LayerMapping

from models import MaapOSMArea, MaapArea


mapping = {'name' : 'name', 
           'geom' : 'LINESTRING', 
} 

def importAreas(filepath, osm=True):
    lm = LayerMapping(MaapArea, filepath, mapping, source_srs=4269)
    for e in lm.layer:
        kwargs = lm.feature_kwargs(e)
        
        # Neccesary hacks to commit geometry data
        kwargs['geom'] = kwargs['geom'].replace('LINESTRING ','POLYGON (')+')'
        kwargs['creator_id'] = 1
        kwargs['editor_id'] = 1
        if osm:
            ma = MaapOSMArea(**kwargs)
        else:
            ma = MaapArea(**kwargs)
        
        ma.save()


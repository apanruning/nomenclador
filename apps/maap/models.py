# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet
from django.contrib.gis.measure import Distance, D
from django.contrib.gis.geos import LineString, MultiLineString, MultiPoint, Point
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.db import models as dbmodels
from django.utils import simplejson
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from djangoosm.models import Nodes as OSMNodes, Streets as OSMStreets, \
                       StreetIntersection as OSMStreetIntersection 
from djangoosm.utils.search import get_location_by_door
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from tagging.fields import TagField
from django.template.defaultfilters import slugify
import mptt
from maap.layers import Point, Area, MultiLine, Layer
from banners.models import TemplateBanner

from cyj_logs.models import SearchLog

def get_closest(geom, exclude_id = None):
    closest_points = MaapPoint.objects.filter(
                        geom__dwithin = (geom, D(m = 500)),
                        closest=True)
    if exclude_id:
        closest_points.exclude(id = exclude_id)
    return closest_points

class MaapMetadata(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

class MaapQuerySet(GeoQuerySet):
    def layer(self):
        elements = self.all()
        objects = []
        for obj in elements:
            objects.append(obj.cast().to_geo_element())
            
        return Layer(elements=objects)

class MaapManager(models.GeoManager):
    def get_query_set(self):
        return MaapQuerySet(self.model)

class Nodes(OSMNodes):
    objects = MaapManager()

    class Meta:
        proxy = True

    def cast(self):
        return self

    def to_layer(self):
        center_point = self.to_geo_element()
        center_point.center = True
        out = get_closest(center_point.geom).layer()
        out.elements.append(center_point)
        return out

    def to_geo_element(self):
        out = Point(
            id = self.id,
            geom = self.geom
        )
        return out


class Streets(OSMStreets):
    objects = MaapManager()

    class Meta:
        proxy = True
    
    def cast(self):
        return self
        
    def get_location_or_street(self, door=None):
        location = get_location_by_door(self.norm, door)
        success = False
        if location:
            point = Point(
                id = 'location_%s_%s' % (self.norm, door),
                name = "%s %s" % (self.name, door),
                geom = location[0],
                center = True,
                clickable = False,
            )

            if location[1] > 0:    
                point.radius = location[1]
            
            layer = Layer(elements = [point])     
            success = True
        else:
            layer = self.to_layer()

        return (layer, success)
        
    def to_layer(self):
        ways = self.ways_set.all()
        
        # Cast ways queryset to multiline 
        ln = []
        for w in ways:
            nodes = [u.node.geom for u in w.waynodes_set.all()]
            ln.append(LineString(nodes))
        
        ml = MultiLineString(ln)
       
        multiline = MultiLine(
            id = 'street_%s' % self.norm,
            name = self.name,
            center = True,
            clickable = False,
            geom = ml
        )
        layer = get_closest(ml).layer()
        layer.id = self.id
        layer.elements.append(multiline)
        
        return layer

        
class MaapModel(models.Model):
    slug = models.SlugField(editable=False, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, editable = False)
    changed = models.DateTimeField(auto_now=True, editable = False)
    creator = models.ForeignKey('auth.User', related_name='created',editable=False) 
    editor = models.ForeignKey('auth.User',related_name='edited', editable=False)
    tags = TagField()
    category = models.ManyToManyField('MaapCategory', null=True, blank=True, related_name='maapmodel_set')
    banner_slots = models.CharField(max_length=255, blank=True, null=True)
    default_layers = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.ForeignKey('MaapMetadata', null=True, blank=True)    
    objects = MaapManager()
        
    class Meta:
        ordering = ('created', 'name',)
    
    @property
    def json_dict(self):
        out = dict(filter(lambda (x,y): not x.startswith('_'), self.__dict__.iteritems()))
        out['created'] = self.created.strftime('%D %T')        
        out['changed'] = self.changed.strftime('%D %T')
        out['absolute_url'] = self.get_absolute_url()
        out['clickable'] = True
        return out

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MaapModel, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        categories = self.category.all()
        if categories:
            cat_slug = categories[0].slug
        else:
            cat_slug = None
        return ('view', [cat_slug, self.id])  

    def to_layer(self):
        # This method only works on inherited models with geom field
        center_point = self.to_geo_element()
        center_point.center = True
        out = get_closest(center_point.geom, self.id).layer()
        out.elements.append(center_point)
        return out

    def cast(self):
        out = self
        try: 
            out = self.maappoint
        except MaapPoint.DoesNotExist:
            pass
        try:
            out = self.maapmultiline
        except MaapMultiLine.DoesNotExist:
            pass
        try:
            out = self.maaparea
        except MaapArea.DoesNotExist:
            pass    
        return out

class MaapCategory(models.Model):
    slug = models.SlugField(unique=True, editable=False)
    name = models.CharField(max_length=35)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    is_public = models.BooleanField(default=True)
    show_all = models.BooleanField(default=False)

    class Meta:
    
        verbose_name_plural = 'MaapCategories'
    
    
    def save(self, *args, **kwargs):        
        if self.id is None:
            num = 0
            while num < 100:
                
                self.slug = slugify(self.name)
                if num > 0:
                    self.slug.append('-%i' % num)
                try:
                    out = super(MaapCategory, self).save( *args, **kwargs)
                    return out
                except:
                    num += 1
        else:
            return super(MaapCategory, self).save(*args, **kwargs)
    
    
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('list_by_category', [self.slug])

class MaapPoint(MaapModel):
   
    geom = models.PointField(srid=settings.DEFAULT_SRID)
    icon = models.ForeignKey('Icon', default=185, blank=True)
    closest = models.BooleanField(default=False)
    popup_text = models.TextField(blank=True)    
    objects = MaapManager()
    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        out['icon'] = self.icon.json_dict
        return Point(**out)

    @models.permalink
    def get_absolute_url(self):
        cat_slug = self.category.all()[0].slug
        return ('view',[cat_slug, self.id])
    

class MaapArea(MaapModel):
    objects = MaapManager()

    geom = models.PolygonField(srid=settings.DEFAULT_SRID)

    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        return Area(**out)   


class MaapZone(MaapArea):
    #nodes_covered = models.ManyToManyField('djangoosm.Nodes', editable=False)
    objects = MaapManager()

    #def save(self, force_insert=False, force_update=False):
    #    super(MaapZone, self).save(force_insert, force_update)
    #    self.nodes_covered = Nodes.objects.filter(geom__coveredby= self.geom)


class MaapMultiLine(MaapModel):
    geom = models.MultiLineStringField(srid = settings.DEFAULT_SRID)
    objects = MaapManager()

    def to_geo_element(self):
        out = self.json_dict
        out.pop('geom')
        out['geom'] = self.geom
        return MultiLine(**out)
        

class Icon(models.Model):
    name = models.CharField(max_length = 100)
    image = models.ImageField(upload_to = "icons")

    def __unicode__( self ):
        return self.name

    @property
    def json_dict(self):
        out = {}
        out['url'] = self.image.url
        out['width'] = self.image.width
        out['height'] = self.image.height
        return out

class PointBanner(TemplateBanner):

    point = models.ForeignKey('MaapPoint', null=True)
    
    def __unicode__(self):
        return slugify('#%s-en-%s' %(self.pk, self.point))
        
    def save(self):
        self.slot = slugify(self.point)
        return super(PointBanner, self).save()

        
try: 
    mptt.register(MaapCategory)  
except mptt.AlreadyRegistered:
    pass


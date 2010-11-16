from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from django.db import connection
from django.utils import simplejson

from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.contrib.gis.geos import LineString, MultiLineString
from osm.models import Streets, WayNodes, Nodes, WayNodesDoor
from utils import synchronize

    
def doors(request):
    '''
    Esta vista devuelve el listado de calles buscables en un selector  
    html y el comportamiento necesario para cuando el usuario elije una calle, 
    el sistema muestre los nodos asociados a la calle elegida 
    '''
    sw =  Streets.objects.all().order_by("name")
    return render_to_response("toolsnmt/waynodeslist.html", 
                               {'streets2':sw,
                                'nodes':[],
                                'street':u'9 de Julio'})

def nodes_by_street(request):
    '''
    Esta vista devuelve el listado de nodos de una calle ademas del codigo 
    para el comportamiento necesario para cuando el usuario elije un nodo este 
    sea mostrado en el mapa
    '''
    street = request.GET['street']
    sw =  Streets.objects.all().order_by("name")
    wnl = WayNodes.objects.filter(way__street__name=street)
    return render_to_response("toolsnmt/waynodeslist.html", 
                               {'nodes':wnl, 
                                'streets2':sw, 
                                'street': unicode(street)})
    
def update_nodes(request):
    '''
    Este metodo actualiza localmente las alturas de los nodos
    '''
    
    street = request.GET['street']
    for k,v in request.GET.iteritems():
        if str(k) != 'street':
            a = WayNodes.objects.get(pk=int(k))
            try:
                if str(v) == 'Editar Valor' or str(v) == '' or not str(v).isdigit():  
                    pass
                else:
                    try:
                        #Caso A: El nodo de altura ya existe. Se guarda el valor nuevo de la altura
                        a.waynodesdoor.number = int(v)
                        a.waynodesdoor.save()
                    except:
                        #Caso B: El nodo de altura no existe. Se crea el nodo y se guarda el valor nuevo
                        b = WayNodesDoor()
                        b.number = int(v)
                        b.waynode = a
                        b.save()
                        
            except:
                    pass
                    
    sw =  Streets.objects.all()
    wnl = WayNodes.objects.filter(way__street__name=street)    
    
    return render_to_response("waynodeslist.html", 
                               {'nodes':wnl,
                                'streets2':sw, 
                                'street': unicode(street) 
                               })
        
def show_street(street):
    way = Streets.objects.get(name=street)
     
    wnl = WayNodes.objects.filter(way__street__name=way.name)    
    points = []
    for p in wnl: 
            pgeom = OGRGeometry(p.node.geom.wkt)
            pgeom.srs = 'EPSG:4326'
            pgeom.transform_to(SpatialReference('EPSG:900913'))
            pcoord = simplejson.loads(pgeom.json)
            point = {
              "type": "point",
              "id": p.node.id,
              "name": p.node.id,
              "geojson": pcoord, 
              "icon": {
                "url": "/media/icons/info.png", 
                "w": 32, 
                "h": 37
                }
            }
            points.append(point)
	            
    return points


def show_street2(request):
    '''
    Esta vista devuelve un JSON representando una capa con puntos (linea)
    '''
    street = request.GET['street']      
    
    wl = Streets.objects.get(name=street).ways_set.all()

    ln = []
    for w in wl:
        ln.append(LineString([u.node.geom for u in w.waynodes_set.all()]))
    
    ml = MultiLineString(ln)   
           
    pgeom = OGRGeometry(ml.wkt)
    pgeom.srs = 'EPSG:4326'
    pgeom.transform_to(SpatialReference('EPSG:900913'))
    lpoints = []
    pcoord = simplejson.loads(pgeom.json)
    lpoints.append({
              "type": "multiline",
              "id": 'multiline', 
              "name": "pipin",
              "geojson": pcoord, 
    
            })
        
    layer = {
            'type': 'layer',
            'id': 'layer-location',
            'elements': lpoints,
            'box_size': None,
            'wnodes': show_street(street),
    }                    
        
    return HttpResponse(simplejson.dumps(layer), mimetype='text/json')  

def show_node(request):
    #Esta vista devuelve un objecto JSON representando un Point
    id_node = request.GET['node']
    node = Nodes.objects.get(pk=id_node)
    pgeom = OGRGeometry(node.geom.wkt)
    pgeom.srs = 'EPSG:4326'
    pgeom.transform_to(SpatialReference('EPSG:900913'))
    pcoord = simplejson.loads(pgeom.json)
    lpoints = []

    point = {
          "type": "point",
          "id": 'point', 
          "name": "pipin",
          "geojson": pcoord, 
          "icon": {
                "url": "/media/icons/info.png", 
                "width": 32, 
                "height": 37
            }
    } 
    lpoints.append(point)
    layer = {
	 'type': 'layer',
         'id': node.id,
         'elements': lpoints,
         'box_size': None
    }
    return HttpResponse(simplejson.dumps(layer), mimetype='text/json')  
    
def synchronize_home(request):
    """
    Este metodo permite sincronizar las alturas cargadas localmente a la estructura de osmosis
    """
   
    return render_to_response("synchronization.html",request)
    
def detail_synchronize(request):
    """ 
    Este metodo ejecuta la sincronizacion y devuelve un detalle del proceso 
    """           
    return render_to_response("detail_synchronize.html",request)
    
def old_streets(request):

    sw = Streets.objects.all()
    street = u'9 de Julio'
    return render_to_response("old_names.html",
                                {'streets2':sw,
                                 'street': street
                                 })

def old_streets_edit(request):
    street = request['street']
        
    sw = Streets.objects.all()
    st = Streets.objects.get(name=street)
    if st.old: 
        name_last_street = st.old
    else:
        name_last_street = "Editar Valor"
    return render_to_response("old_names_edit.html",
                               {'streets2':sw, 
                                'street':unicode(street),
                                'last_name':name_last_street,
                               })    
    
def save_last_name(request):
    sw = Streets.objects.all()
    l_name = request['last_name']
    street = request['street']
    st = Streets.objects.get(name=street)    
    st.old = l_name
    st.save()
        
    return render_to_response("old_streets_edit.html",
                               {'streets2':sw, 
                                'street':unicode(street),
                                'last_name':unicode(l_name)
                               })    

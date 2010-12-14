from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_list, object_detail
from django.template import RequestContext
from django.db import connection
from django.utils import simplejson
from django.contrib.gis.gdal import OGRGeometry, SpatialReference
from django.contrib.gis.geos import LineString, MultiLineString
from maap.models import Streets, Nodes
from maap.layers import Layer
from djangoosm.models import  WayNodes, WayNodesDoor
from utils import synchronize
from django.contrib.auth.decorators import login_required


@login_required()
def doors(request):
    '''
    Esta vista devuelve el listado de calles buscables en un selector  
    html y el comportamiento necesario para cuando el usuario elije una calle, 
    el sistema muestre los nodos asociados a la calle elegida 
    '''
    sw =  Streets.objects.all().order_by("name")
    street = Streets.objects.get(name=u'9 de Julio')
    return render_to_response("toolsnmt/waynodeslist.html", 
                               {'streets2':sw,
                                'nodes':[],
                                'street':street.to_layer().json,
                                'street_name':u'9 de Julio',
                                'layer_points':[]
                                })
@login_required
def nodes_by_street(request):
    '''
    Esta vista devuelve el listado de nodos de una calle ademas del codigo 
    para el comportamiento necesario para cuando el usuario elije un nodo este 
    sea mostrado en el mapa
    '''
    street = Streets.objects.get(name=request.GET['street_name'])
    sw =  Streets.objects.all().order_by("name")
    wnl = WayNodes.objects.filter(way__street__name=street.name)
    nodes = Nodes.objects.filter(waynodes__in=wnl)
    layer = []
    
    for a in nodes:
        b = a.to_layer()
        b.id = a.id
        layer.append(b.json)
    
    return render_to_response("toolsnmt/waynodeslist.html", 
                               {'nodes':wnl, 
                                'streets2':sw, 
                                'street': street.to_layer().json,
                                'street_name': request.GET['street_name'],
                                'layer_points':"["+",".join(layer)+"]"
                                })
    
@login_required
def update_nodes(request):
    '''
    Este metodo actualiza localmente las alturas de los nodos
    '''
    
    for k,v in request.GET.iteritems():
            if str(k) != 'street_name':
                a = WayNodes.objects.get(pk=str(k))
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
                    
    street = Streets.objects.get(name=request.GET['street_name'])
    sw =  Streets.objects.all().order_by("name")
    wnl = WayNodes.objects.filter(way__street__name=street.name)
    nodes = Nodes.objects.filter(waynodes__in=wnl)
    layer = []
    
    for a in nodes:
        b = a.to_layer()
        b.id = a.id
        layer.append(b.json)
                    
    return render_to_response("toolsnmt/waynodeslist.html", 
                               {'nodes':wnl, 
                                'streets2':sw, 
                                'street': street.to_layer().json,
                                'street_name': request.GET['street_name'],
                                'layer_points':"["+",".join(layer)+"]"
                                })


#def synchronize_home(request):
#    """
#    Este metodo permite sincronizar las alturas cargadas localmente a la estructura de osmosis
#    """
   
#    return render_to_response("synchronization.html",request)
    
#def detail_synchronize(request):
#    """ 
#    Este metodo ejecuta la sincronizacion y devuelve un detalle del proceso 
#    """           
#    return render_to_response("detail_synchronize.html",request)
    
#def old_streets(request):

#    sw = Streets.objects.all()
#    street = u'9 de Julio'
#    return render_to_response("old_names.html",
#                                {'streets2':sw,
#                                 'street': street
#                                 })

#def old_streets_edit(request):
#    street = request['street']
        
#    sw = Streets.objects.all()
#    st = Streets.objects.get(name=street)
#    if st.old: 
#        name_last_street = st.old
#    else:
#        name_last_street = "Editar Valor"
#    return render_to_response("old_names_edit.html",
#                               {'streets2':sw, 
#                                'street':unicode(street),
#                                'last_name':name_last_street,
#                               })    
    
#def save_last_name(request):
#    sw = Streets.objects.all()
#    l_name = request['last_name']
#    street = request['street']
#    st = Streets.objects.get(name=street)    
#    st.old = l_name
#    st.save()
        
#    return render_to_response("old_streets_edit.html",
#                               {'streets2':sw, 
#                                'street':unicode(street),
#                                'last_name':unicode(l_name)
#                               })    

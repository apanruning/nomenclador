from osm.models import Streets, Ways, WayNodes, WayNodesDoor, Nodes, RelationMembers, RelationTags, Relations
from django.db import connection, transaction, IntegrityError
from django.db.models import Max
import random
import datetime

def exist_relation_osm(relation_id):
    relations = Relations.objects.filter(id=relation_id).all()
    res = False
        
    if relations.count() != 0:
        return True

    if relations.count() == 0:
        return False
            
def exist_node_in_way(waynode):
    relation_way = RelationMembers.objects.filter(member_id=waynode.way_id,member_type="W").all()[0].relation_id
    nodes_in_relation = RelationMembers.objects.filter(relation=relation_way,member_type='N')
    
    return dict(exist=waynode.node_id in [a.member_id for a in nodes_in_relation], relation=relation_way)
    
def exist_street_in_relations(street):
    street_obj = Streets.objects.get(name=street)
    
    try:
        rm = RelationMembers.objects.filter(member_id=street_obj.ways_set.all()[0].id)[0]
        if ((rm.relation.tags['type'] == u'street_number') and (rm.relation.tags['schemes'] == u'sequential')):
            return True
    except:
        return False
    
def synchronize():
    f = open("osmosis-osm.txt","w")
    f.write(datetime.datetime.now().ctime() + "\n")
    lst_s = []
    info_result = dict(date=datetime.datetime.now().ctime(), length_streets=len(lst_s) , list_streets=lst_s)
    
    exist_node_in_relation = False
    exist_way_in_relation = False
    
    #Obtain all waynodesdoor 
    waynodesdoor = WayNodesDoor.objects.all()

    for wnd in waynodesdoor:
        f.write("%s " %(str(wnd.waynode.way.street)))

        a = RelationMembers.objects.filter(member_id=wnd.waynode.way_id,member_type='W').all()
        rlm = {}
        if a.count() == 1:
            rlm = a[0]
            lst_s.append(rlm)
            exist_way_in_relation = True
            f.write("Exist way in relation: " + str(rlm.relation_id) + "\n" )
        elif a.count() == 0:
            exist_way_in_relation = False
            f.write("Not exist way in relation: " + "\n" )
        else:
            exist_way_in_relation = False
            f.write("Inconsistency: Way in more than one relation \n")
          
        if exist_way_in_relation:    
                max_sequence = RelationMembers.objects.filter(relation=rlm.relation_id).order_by('-sequence_id').all()[0].sequence_id
                
                exist_node = exist_node_in_way(wnd.waynode)
                
                if exist_node['exist']:
                    node_rm = RelationMembers.objects.filter(relation=exist_node['relation'], member_id=wnd.waynode.node_id).all()[0]
                    #update node
                    f.write("Exist node in relation member way \n")                    
                    
                    node_rm.member_role = wnd.number
                    node_rm.save()
                    f.write("Update succesfully relation member: " + str(exist_node['relation']) + "-" + str(node_rm.member_id) + "\n")
            
                if not exist_node['exist']:
                    f.write("Not exist node in relation member way \n")                    
                    max_sequence = RelationMembers.objects.filter(relation=exist_node['relation']).order_by('-sequence_id').all()[0].sequence_id
                
                    #Add node as member to relation
                    relation_member_node = RelationMembers()
                    relation_member_node.relation_id = exist_node['relation']
                    relation_member_node.member_id = wnd.waynode.node_id
                    relation_member_node.member_type = 'N'
                    relation_member_node.member_role = wnd.number
                    relation_member_node.sequence_id = max_sequence + 1
                    relation_member_node.save()
                    
                    f.write("Create relation member node: " + str(exist_node['relation']) + "-" + str(relation_member_node.member_id) + "\n")                       
                    
        if not exist_way_in_relation:
                relation_saved=False
                new_relation = Relations()
                while not(relation_saved):
                    new_relation.id = random.randint(1,999999)
                    exist_relation = exist_relation_osm(new_relation.id)
                    if exist_relation:
                        f.write("already exist relation in osm with id: " + str(new_relation.id) + "\n")
                        f.write("couldn't save \n")
                        f.write("trying again \n")
                        relation_saved = False

                    if not exist_relation:
                        new_relation.version = 1
                        new_relation.user_id = -1
                        new_relation.tstamp = datetime.datetime.now()
                        new_relation.changeset_id = 0

                        try:
                            new_relation.save()
                            f.write("create relation with id: " + str(new_relation.id) + "\n")
                            relation_saved = True
                        except:
                            relation_saved = False

                #Add tag scheme for relation to relation
                relation_tags_node = RelationTags()
                relation_tags_node.relation_id = new_relation.id
                relation_tags_node.k = 'scheme'
                relation_tags_node.v = 'sequential'
                relation_tags_node.save()
                f.write("create relation tag with k field scheme and v field sequential \n")
                #Add tag type street_number to relation
                relation_tags_node = RelationTags()
                relation_tags_node.relation_id = new_relation.id
                relation_tags_node.k = 'type'
                relation_tags_node.v = 'street_number'
                relation_tags_node.save()
                f.write("create relation tag with k field type and v field street_number \n")

                #Add way as member to relation
                relation_member_way = RelationMembers()
                relation_member_way.relation_id =  new_relation.id
                relation_member_way.member_id = wnd.waynode.way_id
                relation_member_way.member_type = 'W'
                relation_member_way.sequence_id = 0
                relation_member_way.save()
                f.write("create relation member way \n")
                
                lst_s.append(relation_member_way)
                
                max_sequence = RelationMembers.objects.filter(relation=new_relation.id).order_by('-sequence_id').all()[0].sequence_id
                                
                #Add node as member to relation
                relation_member_node = RelationMembers()
                relation_member_node.relation_id =  new_relation.id
                relation_member_node.member_id = wnd.waynode.node_id
                relation_member_node.member_type = 'N'
                relation_member_node.member_role = wnd.number
                relation_member_node.sequence_id = max_sequence + 1
                relation_member_node.save()
                f.write("create relation member node \n")
                
      
    info_result.update(length_streets=len(lst_s))  
    return info_result

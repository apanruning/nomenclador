/**window.onload=function(){
     include(MEDIA_URL+'/modules/state.js');
     
}  **/


$(document).ready(
    //initilize system
    function(){
        //load modules. Note that the order is important
        include(MEDIA_URL+'/modules/state.js');  
        include(MEDIA_URL+'/modules/map_settings.js');  

        //settings for map's options
map_options = {
           'projection' : new OpenLayers.Projection("EPSG:900013"),
           'maxResolution' : 200000.0002,
           'displayProjection' : new OpenLayers.Projection("EPSG:4326"),
           'units' : "m"
            }    
        //create map whith map options     
        map = new OpenLayers.Map('map', map_options);

        //update the state variable
        state['map'] = map

        //load modules
        include(MEDIA_URL+'/modules/point.js');
        include(MEDIA_URL+'/modules/init.js');

        //Start execution        
        init_phase_one();
        init_phase_two();
    } 

)	



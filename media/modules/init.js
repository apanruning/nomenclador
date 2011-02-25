/*** 
    This module extends the state layer to set specific initialization 
    functions to state 
***/

// This funcion hide what layers must be available in the switcher-layers 
// control map when the map is shown
Maap.State.prototype.initializeBaseLayers = function() {
    layerMapnik = new OpenLayers.Layer.OSM.Mapnik(
            "OpenStreetMap (Mapnik)",
            {layers: 'basic'}
    );
    this.map.addLayer(layerMapnik); 
    this.base_layers = this.base_layers.concat(layerMapnik);
    
    return 0;
}

// This funcion set the initial bounds for map
Maap.State.prototype.initializeBounds = function() {
    //change this values for change de level zoom
    this.map.zoomToExtent(
        new OpenLayers.Bounds(
            -7160964.775099885,
            -3693704.7356770867,
            -7130772.148932681,
            -3678417.3300227895
        ),
        true
    );
    return 0;
}

// This function initialize the control objects of state 
Maap.State.prototype.initializeControls = function () {
    //add and/or remove controls to map
    this.map.addControl(new OpenLayers.Control.PanZoomBar());
    //this.map.addControl(new OpenLayers.Control.OverviewMap());
    this.map.addControl(new OpenLayers.Control.Navigation()); 
    this.map.addControl(new OpenLayers.Control.Attribution());
    this.map.addControl(new OpenLayers.Control.MousePosition());
    this.map.addControl(new OpenLayers.Control.Permalink());
    this.map.addControl(new OpenLayers.Control.LayerSwitcher({'ascending':false}));


    return 0;
}


// This function initialize all settings of state. 
Maap.State.prototype.init = function() {

    //add initial layers to map
    this.initializeBaseLayers();

    //center the map in Cordoba position
    //map.setCenter(cordoba, 19);

    //load controls to map
    this.initializeControls();

    //set the level to the user can see the map. (zoom)        
    this.initializeBounds(); 

    return 0;

}
        


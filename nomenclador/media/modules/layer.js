/***
    This module handles layers, and other elements, evaluating from json standard model representation    
***/

/*
------------- 
 OBJECT Layer
-------------
*/
// Initialization function for object Layer
Maap.Layer = function (metadata, map) {
    for (m in metadata) {
        this[m] = metadata[m];
    }
    var elms = new Array();
    
    for (i=0;i< this.elements.length; i++) {
        if (this.elements[i].type == 'point') {
            elm = new Maap.Point(this.elements[i])
        } else if (this.elements[i].type == 'multiline') {
            elm = new Maap.MultiLine(this.elements[i])
        } else if (this.elements[i].type == 'area') {
            elm = new Maap.Area(this.elements[i])
        }
        // Set controls
        //var control = new OpenLayers.Control.SelectFeature(elm.layer);
        //this.map.addControl(control);
        //control.activate();
        elms.push(elm);
    };
    
    this.elements = elms;   
   
}

// Methods and extra attributes for object Layer
Maap.Layer.prototype = {
    
    boxCenter: function() {
        b = this.box_size
        map.zoomToExtent(new OpenLayers.Bounds(b[0],b[1],b[2],b[3]),true)
    },
    
    getLayers: function() {
        out = new Array();
        for (i=0; i < this.elements.length; i++) {
            out.push(this.elements[i].layer);
        };
        return out;
    },
    
    show: function() {
        for (i=0; i< this.elements.length; i++) {
            this.elements[i].show();
        };
        this.boxCenter();
    },
    
    hide: function() {
        for (i=0; i< this.elements.length; i++) {
            this.elements[i].hide();
        }
    }
};


// Extends Maap.State functionality: Add Layer
Maap.State.prototype.setLayer = function(data) {
    // Eval layer object
    Layer = new Maap.Layer(data, state.map);          
    state.map.addLayers(Layer.getLayers());
    state.layers[Layer.id] = Layer;
    return Layer;
};


// Extends Maap.State functionality: Add Layer
Maap.State.prototype.loadLayer = function(url, reload, callback) {
    state = this;
    
    //send request to server for get the layer to add 
    $.getJSON(url, 
        function(data) {
            Layer = state.setLayer(data);
            callback(Layer);
        }
    );
    return 0;
};

// Extends Maap.State functionality: Add Point to Map
Maap.State.prototype.loadPoint = function(url, reload, callback) {
    state = this;

    //send request to server for add layer of point
    $.getJSON(url, 
        function(data) {
            // Eval point object
           var ins = new Maap.Point(data);
           state.map.addLayer(ins.layer);
           callback(ins);
            }
    );
    
   return false;
 };



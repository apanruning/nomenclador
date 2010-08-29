/***
    This module handles layers, and other elements, evaluating from json standard model representation    
***/

/* Style Map */

        this.styleMap = new OpenLayers.StyleMap();


/*
------------- 
 OBJECT Layer
-------------
*/
// Initialization function for object Layer
Maap.Layer = function (metadata, map) {
    for (m in metadata) {
        this[m] = metadata[m];
        this.map = map;
    }
    // start stylemap
    this.stylemap = new OpenLayers.StyleMap();
    this.layer = new OpenLayers.Layer.Vector(this.id, {styleMap:this.stylemap});

    var elms = new Array();
    
    for (i=0;i< this.elements.length; i++) {
        if (this.elements[i].type == 'point') {
            elm = new Maap.Point(this.elements[i])
        } else if (this.elements[i].type == 'multiline') {
            elm = new Maap.MultiLine(this.elements[i])
        } else if (this.elements[i].type == 'area') {
            elm = new Maap.Area(this.elements[i])
        }

        // insert element styles to base style
        var st;
        for (st in elm.style)
            this.style[st] = elm.style[st];      

        // insert features to base layer
        this.layer.addFeatures(elm.features);
        this.layer.events.register("featureselected", elm.features[0], 
             function(evt) { 
             alert(elm.name);
             });

        elms.push(elm);
    };
    
    // add default rules with collected feature styles
    this.stylemap.addUniqueValueRules("default", "style", this.style);
    /*
    var control = new OpenLayers.Control.SelectFeature(this.layer);
    this.map.addControl(control);
    control.activate();
    */
 
    this.elements = elms;   
   
}

// Methods and extra attributes for object Layer
Maap.Layer.prototype = {
    style: { 
        'area': {
            strokeColor: '#ff333f',
            strokeWidth: 1, 
            fillColor: '#f0aa22',
            fillOpacity: 0.3,
            strokeDashstyle: 'dashdot'
        },
        'line': {
            strokeColor: '#feff00',
            strokeOpacity: 0.8,
            strokeWidth: 5
        },
        'line-border': {
            strokeColor: '#612000',
            strokeOpacity: 0.2,
            strokeWidth: 8
        }       
    },
    boxCenter: function() {
        b = this.box_size;
        this.map.zoomToExtent(new OpenLayers.Bounds(b[0],b[1],b[2],b[3]),true);
    },
    
    getLayers: function() {
    /*
        out = new Array();
        for (i=0; i < this.elements.length; i++) {
            out.push(this.elements[i].layer);
        };
        return out;
    */
        return [this.layer];
    },
    show: function() {
        /*
        for (i=0; i< this.elements.length; i++) {
            this.elements[i].show();
        };
        */
        this.layer.setVisibility(true);
        this.boxCenter();
    },
    
    hide: function() {
        /*
        for (i=0; i< this.elements.length; i++) {
            this.elements[i].hide();
        }
        */
        this.layer.setVisibility(false);
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



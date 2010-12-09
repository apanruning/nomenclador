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

        elms.push(elm);
    }
    
    // add default rules with collected feature styles
    this.stylemap.addUniqueValueRules("default", "style", this.style);

    // add event listeners
    this.layer.events.on({
        "featureselected": this.onSelect,
        scope: this.layer
    });

    var selectCtrl = new OpenLayers.Control.SelectFeature(this.layer);
    var highlightCtrl = new OpenLayers.Control.SelectFeature(this.layer, {
        hover: true,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
            featurehighlighted: this.onHover,
            featureunhighlighted: this.onUnhover
        }
    });

    this.map.addControl(highlightCtrl);
    this.map.addControl(selectCtrl);
    highlightCtrl.activate();
    selectCtrl.activate();

 
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
    onSelect: function(evt) {
        var maap = evt.feature.attributes.maap;
        if (maap.clickable && maap.absolute_url) {    
            window.location = maap.absolute_url;
        }
    },
    onHover: function(evt) {
        var maap = evt.feature.attributes.maap;  
        if (maap.popup_text) {    
            var popup = new OpenLayers.Popup.FramedCloud(maap.name, 
                             evt.feature.geometry.getBounds().getCenterLonLat(),
                             null,
                             "<h2>" + maap.name +"</h2>"+maap.popup_text,
                             null, true);
            evt.feature.popup = popup;
            this.map.addPopup(popup);
        }
    },
    onUnhover: function(evt) {
        var maapelem = evt.feature.attributes.maap;
        var mep = this.map;
        if (maapelem.popup_text) {
            setTimeout(function() {
                mep.removePopup(evt.feature.popup);
                evt.feature.popup.destroy();
                evt.feature.popup = null;
            }
            , 1000);
        }
    },
    boxCenter: function() {
        b = this.box_size;
        this.map.zoomToExtent(new OpenLayers.Bounds(b[0],b[1],b[2],b[3]),true);
    },
    getLayers: function() {
        return [this.layer];
    },
    show: function() {
        this.layer.setVisibility(true);
        this.boxCenter();
    },
    
    hide: function() {
        this.layer.setVisibility(false);
    },
    toogle: function() {
        if (this.layer.getVisibility() == true) {
            this.hide();    
        } else {
            this.show();
        }
    },
};


// Extends Maap.State functionality: Add Layer
Maap.State.prototype.setLayer = function(data) {
    // Eval layer object
    Layer = new Maap.Layer(data, state.map);          
    state.map.addLayers(Layer.getLayers());
    state.layers[Layer.id] = Layer;
    return Layer;
};


// Extends Maap.State functionality: Load Layer
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

// Extends Maap.State functionality: Show/Hide layer in Map
Maap.State.prototype.toogleLayer = function(url, reload, callback) {
    state = this;
    alert(state.layers);

    
    for (j=0;j<state.layers.length;j++) {
        if (state.layers[j].name==url) {
            if (state.layers[j].getVisibility()==true) {
                state.layers[j].display(false);
                state.layers[j].visibility = false;
                state.map.zoomIn();
                state.map.zoomOut();
                
            } else {
                state.layers[j].display(true);
                state.layers[j].visibility = true;
                 state.map.zoomIn();
                 state.map.zoomOut();
            }
            break;       
       } else {
            continue;
       }
    }
    
    callback(state);
        
    return false;
 };

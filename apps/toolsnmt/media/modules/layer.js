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
    },
};


// Extends Maap.State functionality: Add Layer
Maap.State.prototype.setLayer = function(data) {
    // Eval layer object
    var Layer = new Maap.Layer(data, state.map);          
    state.map.addLayers(Layer.getLayers());
    state.layers.push(Layer);
    return Layer;
};


// Extends Maap.State functionality: Add Layer
Maap.State.prototype.loadLayer = function(url, reload, callback) {
    state = this;
    
    //send request to server for get the layer to add 
    $.getJSON(url, 
        function(data) {
            var Layer = state.setLayer(data);
            for(i=0;i<data.wnodes.length;i++){
                var p = data.wnodes[i]
                var markers = new OpenLayers.Layer.Markers(p.id+='',{'visibility':false});
           	 
           	    state.map.addLayer(markers);
            	state.layers.push(markers);
            	
                var size = new OpenLayers.Size(p.icon.w,p.icon.h);
                var offset = new OpenLayers.Pixel(-size.w/2, -size.h/2);
                var icon = new OpenLayers.Icon(p.icon.url,size,offset.offset());
                var lonlat = create_position(p.geojson.coordinates[0],p.geojson.coordinates[1]);
                var marker = new OpenLayers.Marker(lonlat, icon);
                markers.addMarker(marker);
	    }
    
            callback(Layer);
        }
    );
    return 0;
};

// Extends Maap.State functionality: Show/Hide layer in Map
Maap.State.prototype.toogleLayer = function(url, reload, callback) {
    state = this;
    // Verify state
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



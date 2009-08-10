/*
------------
 OBJECT Area
------------
*/

// Methods and extra attributes for object

Maap.Area = Maap.Geom.extend({
    init: function(metadata) {
        this._super(metadata);
        geojson_format = new OpenLayers.Format.GeoJSON();
        var styleMap = new OpenLayers.StyleMap({strokeColor: '#ff333f', fillColor: '#f0aa22'});
        this.layer = new OpenLayers.Layer.Vector(this.id,{styleMap:styleMap});
        this.layer.addFeatures(geojson_format.read(this.geojson));
            
    }
})



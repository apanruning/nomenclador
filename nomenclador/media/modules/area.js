/*
------------
 OBJECT Area
------------
*/

// Methods and extra attributes for object

Maap.Area = Maap.extend(Maap.Geom, {
    init: function() {
        geojson_format = new OpenLayers.Format.GeoJSON();
        this.layer = new OpenLayers.Layer.Vector(this.id);     
        this.layer.addFeatures(geojson_format.read(this.geojson));
            
    }
})


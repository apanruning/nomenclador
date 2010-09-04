/*
------------
 OBJECT Area
------------
*/

// Methods and extra attributes for object

Maap.Area = Maap.Geom.extend({
    init: function(metadata) {
        this._super(metadata);
        this.features = Array();
        var geojson_format = new OpenLayers.Format.GeoJSON();
        var geom = geojson_format.read(this.geojson,"Geometry");

        this.features.push(new OpenLayers.Feature.Vector(
            geom,
            {style: 'area', maap:this}
        ));            
    }
});



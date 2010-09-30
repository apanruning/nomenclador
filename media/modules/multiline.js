/*
-----------------
 OBJECT Multiline
-----------------
*/

// Methods and extra attributes for object

Maap.MultiLine = Maap.Geom.extend({
    init: function(metadata) {
        this._super(metadata);
        
        var geojson_format = new OpenLayers.Format.GeoJSON();
        
        var geom = geojson_format.read(this.geojson,"Geometry");

        this.features = new Array();
        this.features.push(new OpenLayers.Feature.Vector(geom.clone(),
            {style: 'line-border',
            maap:this}
        ));
        this.features.push(new OpenLayers.Feature.Vector(geom.clone(),
            {style: 'line',
            maap:this}
        ));
    }
});



/*
-----------------
 OBJECT Multiline
-----------------
*/

// Methods and extra attributes for object

Maap.MultiLine = Maap.Geom.extend({
    init: function(metadata) {
        this._super(metadata);
        
        geojson_format = new OpenLayers.Format.GeoJSON();
        
        var geom = geojson_format.read(this.geojson,"Geometry");
        var lookup = {
            'line': {
                strokeColor: '#feff00',
                strokeOpacity: 0.8,
                strokeWidth: 5
            },
            'border':{
                strokeColor: '#612000',
                strokeOpacity: 0.2,
                strokeWidth: 8
            }
        }
        var features = new Array();
        features.push(new OpenLayers.Feature.Vector(geom.clone(),
            {style: 'border'}
        ))
        features.push(new OpenLayers.Feature.Vector(geom.clone(),
            {style: 'line'}
        ))

        var styleMap = new OpenLayers.StyleMap();
        styleMap.addUniqueValueRules("default", "style", lookup);
        this.layer = new OpenLayers.Layer.Vector(this.id,{styleMap:styleMap});
        this.layer.addFeatures(features);
        this.layer.events.register("featureselected", features[0], function(evt) { alert(evt);});
    }
});



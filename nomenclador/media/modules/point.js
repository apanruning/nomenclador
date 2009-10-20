/*
------------- 
 OBJECT Point
-------------
*/

// Methods and extra attributes for object

Maap.Point = Maap.Geom.extend({
    init: function(metadata) {
        this._super(metadata);

        var geojson_format = new OpenLayers.Format.GeoJSON();        
        var pgeom = geojson_format.read(this.geojson,"Geometry");
        var lookup = {};
        var features = new Array();
        var styleMap = new OpenLayers.StyleMap();
                
        if (this.radius) {
            var geom = OpenLayers.Geometry.Polygon.createRegularPolygon(
                pgeom,
                this.radius,
                50
            );
            
            lookup['line'] = {
                strokeColor: '#f3be4b',
                strokeOpacity: 0.8,
                strokeWidth: 1,
                fillColor: 'yellow',
                fillOpacity: 0.2
            };
           
            features.push(new OpenLayers.Feature.Vector(
                geom,
                {style: 'line'}
            ));
        };

        lookup['marker'] = {
            externalGraphic: this.icon.url,
            graphicWidth: this.icon.width,
            graphicHeight: this.icon.height,
            graphicOpacity: 1,
            graphicXOffset: -(this.icon.width/2),
            graphicYOffset: -(this.icon.height)+2
        };

        features.push(new OpenLayers.Feature.Vector(
            pgeom,
            {style: 'marker'}
        ));            
        

        styleMap.addUniqueValueRules("default", "style", lookup);
        this.layer = new OpenLayers.Layer.Vector(this.id,{styleMap:styleMap});
        this.layer.addFeatures(features);
    }
})






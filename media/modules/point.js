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

        this.features = new Array();
        this.style = {};
        
        
        // If point have radius        
        if (this.radius) {
            var geom = OpenLayers.Geometry.Polygon.createRegularPolygon(
                pgeom,
                this.radius,
                50 //opacity
            );
            
            this.style['point_radius_'+this.id] = {
                strokeColor: '#f3be4b',
                strokeOpacity: 0.1,
                strokeWidth: 1,
                fillColor: 'yellow',
                fillOpacity: 0.2
            };
           
            this.features.push(new OpenLayers.Feature.Vector(
                geom,
                {style: 'point_radius_'+this.id}
            ));
        };

        this.style['point_'+this.id] = {
            externalGraphic: this.icon.url,
            graphicWidth: this.icon.width,
            graphicHeight: this.icon.height,
            graphicOpacity: 1,
            graphicXOffset: -(this.icon.width/2),
            graphicYOffset: -(this.icon.height)+2
        };

        this.features.push(new OpenLayers.Feature.Vector(
            pgeom,
            {style: 'point_'+this.id}
        )); 
    }
})






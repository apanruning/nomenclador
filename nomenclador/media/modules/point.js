/*
------------- 
 OBJECT Point
-------------
*/

// Methods and extra attributes for object

Maap.Point = Maap.Geom.extend({
    init: function(metadata) {
        this._super(metadata);
        size = new OpenLayers.Size(this.icon.width, this.icon.height);
        offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
        icon = new OpenLayers.Icon(this.icon.url, size, offset);
        lonlat = new OpenLayers.LonLat(this.geojson.coordinates[0],this.geojson.coordinates[1]);
        marker = new OpenLayers.Marker(lonlat, icon);
        this.layer = new OpenLayers.Layer.Markers();     
        this.layer.addMarker(marker);    
    }
})




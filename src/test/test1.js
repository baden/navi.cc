// These are SVG-related namespace URLs
var SVG = {};
SVG.ns = "http://www.w3.org/2000/svg";
SVG.xlinkns = "http://www.w3.org/1999/xlink";

var MarkersOverlay = function(map, data){
    this.setMap(map);
    this.data = data;
};

MarkersOverlay.prototype = new google.maps.OverlayView();

MarkersOverlay.prototype.onAdd = function() {
    console.log("MarkersOverlay.onAdd");
    // Create the DIV and set some basic attributes.
    var div = document.createElement('DIV');
    div.style.position = "absolute";
    div.style["-webkit-transform"] = "translateZ(0)";
    this.getPanes().overlayLayer.appendChild(div);

    this.div_ = div;
}


MarkersOverlay.prototype.draw = function() {
    console.log("MarkersOverlay.draw", this.div_);
    var overlayProjection = this.getProjection();
    for(i=0; i<this.data.length; i++){
        var d = this.data[i];
        var pos = overlayProjection.fromLatLngToDivPixel(d.pos);
        if(!d.div) {

            //var direction = document.createElement('svg');
            var svg = d.div = document.createElementNS(SVG.ns, "svg:svg");
            svg.setAttribute("style", 'margin: -8px -8px -15px -4px');
            svg.style.position = "absolute";
            svg.setAttribute("width", '32px');
            svg.setAttribute("height", '32px');
            svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", SVG.xlinkns);

            var g = document.createElementNS(SVG.ns, "g");
            g.setAttributeNS(null, 'transform', 'translate(16,16)');

            var shape = document.createElementNS(SVG.ns, "polyline");
            shape.setAttributeNS(null, "points", "-7,-11 0,-15 7,-11");
            shape.setAttributeNS(null, "fill", "none");
            shape.setAttributeNS(null, "stroke", "black");
            shape.setAttributeNS(null, "stroke-width", "2px");
            shape.setAttributeNS(null, 'transform', 'rotate(' + d.course + ')');

            g.appendChild(shape);
            svg.appendChild(g);

            /*var div = d.div = document.createElement('DIV');
            div.setAttribute("class", "lastmarker spritecolor-red sprite-cycling");
            div.style.position = "absolute";
            div.style["-webkit-transform"] = "translateZ(0)";*/

            /*var c = document.createElement('circle');
            c.setAttribute("r", 20);
            c.setAttribute("cx", 10);
            c.setAttribute("cy", 10);
            div.appendChild(c);*/
            //div.appendChild(svg);

            this.div_.appendChild(svg);
        }
        d.div.style.left = '' + (pos.x - 8) + 'px';
        d.div.style.top = '' + (pos.y - 8) + 'px';
    }
}


function initialize() {
    var latlng = new google.maps.LatLng(48.497, 34.944);
    var myOptions = {
        zoom: 11,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    var div = document.getElementById('map');
    var map = new google.maps.Map(div, myOptions);

    var data = [];
    for(var i=0; i<10000; i++){
        var l = {
            pos: new google.maps.LatLng(48.5 + 0.4 * (Math.random() - 0.5), 34.95 + 0.8 * (Math.random() - 0.5)),
            course: 360.0 * Math.random()
        }
        data.push(l);
    }

    var overlay = new MarkersOverlay(map, data);

};

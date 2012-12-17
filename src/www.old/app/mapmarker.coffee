# Нужно переделать из google.maps.OverlayView на маркер на
# Один google.maps.OverlayView на все маркеры
#

class LastMarkers
    markers = {}
    doms = {}
    overlay = null

    constructor: (@map) ->
        console.log 'LastMarkers:constructor', @map
        overlay = new google.maps.OverlayView()

        listener = google.maps.event.addListener(@map, 'bounds_changed', () ->
            #log '+fire bounds_changed', map.getBounds()
        )

        overlay.onAdd = ->
            console.log 'LastMarkers:onAdd'

            layer = document.createElement 'div'
            layer.style["-webkit-transform"] = "translateZ(0)";
            layer.style.position = "absolute";
            @getPanes().overlayLayer.appendChild layer

            #layer = d3.select(@getPanes().overlayLayer).append("div").attr("class", "stations")
            #svg = layer.append("svg:svg").attr("class", "marker")

            console.log '== LastMarkers layes=', layer, svg

            overlay.draw = ->
                ###
                # update existing markers
                console.log 'LastMarkers:draw'  # , markers
                transform = (d) ->
                    d = new google.maps.LatLng(d.value.lat, d.value.lon)
                    d = projection.fromLatLngToDivPixel(d)
                    d3.select(this).style("left", (d.x - padding) + "px").style "top", (d.y - padding) + "px"
                projection = @getProjection()
                padding = 40
                marker = layer.selectAll("svg").data(d3.entries(markers)).each(transform).enter().append("svg:svg").each(transform).attr("class", "marker")
                marker.append("svg:circle").attr("r", 20).attr("cx", padding).attr "cy", padding
                marker.append("svg:text").attr("x", padding + 7).attr("y", padding).attr("dy", ".31em").text (d) ->
                    d.key
                ###
                projection = @getProjection()
                for k, v of markers
                    #console.log 'k, v=', k, v
                    divpx = projection.fromLatLngToDivPixel(new google.maps.LatLng(v.lat, v.lon))

                    #if !v.div
                    if !doms[k]
                        #v.div = document.createElement 'div'
                        #v.div.setAttribute "class", "mymarker"
                        #layer.appendChild v.div

                        doms[k] = document.createElement 'div'
                        doms[k].setAttribute "class", "lastmarker spritecolor-red sprite-cycling"
                        doms[k].style["-webkit-transform"] = "translateZ(0)";
                        doms[k].style.position = "absolute";
                        doms[k].style.backgroundColor = "red";
                        layer.appendChild doms[k]
                    doms[k].style.left = divpx.x - 8 + 'px';
                    doms[k].style.top = divpx.y - 8 + 'px';
                    #v.div.setAttribute("style", "-webkit-transform")

                console.log 'LastMarkers:draw end'


        overlay.setMap(@map)

    setMarker: (k, v) ->
        markers[k] = v
        #    lat: v.lat
        #    lon: v.lon


    redraw: ->
        if overlay.draw
            overlay.draw()


window.LastMarkers = LastMarkers
#console.log 'mapmarker=', MapMarker


class MapMarker extends google.maps.OverlayView
    constructor: (@map) ->
        #console.log 'MapMarker:constructor', @map
        @div = null
        @arrdiv = null
        # @this.onclick = onclick
        @title = null
        @point = null
        @infowindow = null
        @skey = null
        @setMap(@map)

    onAdd: ->
        #console.log 'MapMarker:onAdd', @map
        div = document.createElement 'div'
        div.marker = @
        div.setAttribute "class", "mymarker"
        #div.style.border = 'none'
        #div.style.borderWidth = '0px'
        #div.style.position = 'absolute'
        arrdiv = document.createElement 'div'
        arrdiv.setAttribute "class", "mymarker-arrow"
        div.appendChild arrdiv

        div.addEventListener( 'click', (e) ->
            @.marker.Info()
        , false)
        div.addEventListener( 'mouseout', (e) ->
            arrdiv = document.getElementById "arrowdiv"
            if arrdiv
                arrdiv.style.display = "none"
        , false)

        #img = document.createElement 'img'
        #img.src = @img_
        #img.style.width = '100%'
        #img.style.height = '100%'
        #div.appendChild img

        @div = div
        @arrdiv = arrdiv

        panes = @getPanes()
        this.panes = panes
        panes.overlayLayer.appendChild div

    draw: ->
        #console.log 'MapMarker:draw', @map
        ###
        overlayProjection = @getProjection()
        sw = overlayProjection.fromLatLngToDivPixel(@bounds_.getSouthWest())
        ne = overlayProjection.fromLatLngToDivPixel(@bounds_.getNorthEast())

        div = @div_
        div.style.left = sw.x + 'px'
        div.style.top = ne.y + 'px'
        div.style.width = (ne.x - sw.x) + 'px'
        div.style.height = (sw.y - ne.y) + 'px'
        ###
        if @point
            # Size and position the overlay. We use a southwest and northeast
            # position of the overlay to peg it to the correct position and size.
            # We need to retrieve the projection from this overlay to do this.
            overlayProjection = @getProjection()
            #console.log 'overlayProjection =', overlayProjection
            if not overlayProjection
                return

            # Retrieve the southwest and northeast coordinates of this overlay
            # in latlngs and convert them to pixels coordinates.
            # We'll use these coordinates to resize the DIV.
            divpx = overlayProjection.fromLatLngToDivPixel(@point);
            # var lng = overlayProjection.fromLatLngToDivPixel(this.point.lng());

            # Resize the image's DIV to fit the indicated dimensions.
            div = @div
            div.style.left = divpx.x - 8 + 'px'
            div.style.top = divpx.y - 8 + 'px'

            @arrdiv.setAttribute("style", "-webkit-transform: rotate(" + @point.angle + "deg);z-index:-1;")

    onRemove: ->
        #@div_.parentNode.removeChild(@div_)
        #@div_ = null
        @div.removeChild @arrdiv
        @div.parentNode.removeChild @div
        @arrdiv = null
        @div = null

    setPosition: (point) ->
        #console.log 'MapMarker:setPosition', @map
        #  log('Marker change position');
        @point = point
        #  console.log('MyMarker.protorype.setPosition');
        #@setTitle(dt_to_datetime(point.date));
        @draw()

    hide: ->
        if @div
            @div.style.visibility = 'hidden'

    show: ->
        if @div
            @div.style.visibility = 'visible'

    toggle: ->
        if @div
            if @div.style.visibility is 'hidden'
                @show()
            else
                @hide()

    toggleDOM: ->
        if @getMap()
            @setMap null
        else
            @setMap @map

window.MapMarker = MapMarker
#console.log 'mapmarker=', MapMarker


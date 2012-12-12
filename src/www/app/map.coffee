# Модуль работы с виджетом карты
'use strict'
config = config.map or {}
log "TODO: remove config=", config

MapModule = angular.module 'map', ['ngResource', 'ui']

MapModule.value "ui.config", {
    date:
        regional: "ru"
}

MapModule.run ["$rootScope", ($rootScope) ->
    #log 'MapModule.run', $rootScope

    $rootScope.$on '$locationChangeSuccess', ($scope, $location, $route) ->
        #log '$locationChangeSuccess',
        #  $scope, $rootScope, typeof($location), typeof($route)
        if $location.match(/\/map/)
            #log '==MAP'
            if config.map
                google.maps.event.trigger config.map, 'resize'
]

MapModule.controller "mapControl", [
    "$scope"
    "$rootScope"
    "Systems"
    ($scope, $rootScope, Systems) ->
        $scope.show = true
        $scope.markers = {}
        $scope.systems = Systems
        # Systems.systems
        $scope.name ='misko'
        log 'Scope=', $scope, Systems, $scope.systems
        ###
        $scope.$watch 'name', (newValue, oldValue) ->
            console.log '====== watch:name:', oldValue, newValue

        ###

        $scope.$watch( "systems", (nv, ov) ->
                #console.log '****> changed:', nv, ov
                for k, v of nv.systems
                    if v.last.point
                        #console.log 'v=', v.last.point
                        if not $scope.markers[k]
                            $scope.markers[k] = new MapMarker(window.config.map)
                        $scope.markers[k].setPosition(new google.maps.LatLng(v.last.point.lat, v.last.point.lon))
                        #v.marker = marker
            true)


        #$scope.$digest()
        $scope.hide = () ->
            $scope.show = !$scope.show
            $scope.systems.push new google.maps.LatLng(48.5, 34.5)
            #Systems.systems.push new google.maps.LatLng(48.5, 34.5)
            $scope.name = 'mikle'
            #$scope.$digest()
            console.log 'markers=', $scope.systems
            if config.map
                setTimeout ( () ->
                    google.maps.event.trigger config.map, 'resize'
                    console.log '#############-+> mmmap.api', $rootScope.api
                ), 1000
                #setTimeout () ->
]


MapModule.directive 'map', () ->
    {
        restrict: 'E'
        replace: true
        transclude: true
        template: '<div class="mapCanvas"></div>'
        link: ($scope, element, attrs, controller) ->
            #log 'map:link', $scope, element, attrs, controller
            latlng = new google.maps.LatLng 48.497, 34.944
            myOptions = {
                zoom: 11
                center: latlng
                mapTypeId: google.maps.MapTypeId.ROADMAP
                # disableDefaultUI: true
                ###
                overviewMapControl: true,
                scaleControl: false,
                rotateControl: false,
                zoomControl: false,
                streetViewControl: false,
                panControl: false###
            }
            map = config.map = new google.maps.Map element[0], myOptions
            console.log 'map=', config.map
            setTimeout ( () ->
                console.log 'create-test-marker'
                marker = window.marker = new MapMarker(map)
                marker.setPosition(new google.maps.LatLng(48.5, 34.5))
            ), 1000


            # Load the station data. When the data comes back, create an overlay.
            #d3.json "fakeapi/stations.json", (data) ->
            d3.json "api/lasts.json", (data) ->
                console.log '==stations.json', data
                overlay = new google.maps.OverlayView()
                listener = google.maps.event.addListener(map, 'bounds_changed', () ->
                    log '+fire bounds_changed', map.getBounds()
                    count = 0
                    for k, v of data.lasts
                        #log 'v=', v
                        #break
                        if map.getBounds().contains(new google.maps.LatLng(v[0], v[1]))
                            count += 1
                    log 'count = ', count
                    #setupWeatherMarkers();
                    #google.maps.event.removeListener(listener)
                )

                # Add the container when the overlay is added to the map.
                overlay.onAdd = ->
                    layer = d3.select(@getPanes().overlayLayer).append("div").attr("class", "stations")
                    svg = layer.append("svg:svg").attr("class", "marker")
                    console.log 'svg=', svg

                    # Draw each marker as a separate SVG element.
                    # We could use a single SVG, but what size would it have?
                    overlay.draw = ->
                        # update existing markers

                        # Add a circle.

                        # Add a label.
                        transform = (d) ->
                            d = new google.maps.LatLng(d.value[0], d.value[1])
                            d = projection.fromLatLngToDivPixel(d)
                            d3.select(this).style("left", (d.x - padding) + "px").style "top", (d.y - padding) + "px"
                        projection = @getProjection()
                        padding = 10
                        marker = layer.selectAll("svg").data(d3.entries(data.lasts)).each(transform).enter().append("svg:svg").each(transform).attr("class", "marker")
                        marker.append("svg:circle").attr("r", 4.5).attr("cx", padding).attr "cy", padding
                        marker.append("svg:text").attr("x", padding + 7).attr("y", padding).attr("dy", ".31em").text (d) ->
                            d.key



                # Bind our overlay to the map…
                overlay.setMap map


        ###
        controller: ["$scope", "$route", ($scope, $route) ->
            log '== MAP:controller', $scope, $route
            $scope.hide = () ->
                log 'hide me'
        ]
        ###
    }



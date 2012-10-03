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
    "$scope", ($scope) ->
        $scope.show = true
        $scope.hide = () ->
            $scope.show = !$scope.show
            if config.map
                setTimeout ( () ->
                    google.maps.event.trigger config.map, 'resize'
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
            config.map = new google.maps.Map element[0], myOptions
        ###
        controller: ["$scope", "$route", ($scope, $route) ->
            log '== MAP:controller', $scope, $route
            $scope.hide = () ->
                log 'hide me'
        ]
        ###
    }



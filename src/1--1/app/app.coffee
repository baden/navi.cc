'use strict'

# gpsModule = angular.module 'gpsModule', ['map', 'todo', 'LogModule']

gpsModule = angular.module 'gpsModule', ['map', 'log', 'ui', 'config']
gpsModule.controller "navigationCtrl", ($scope, $location) ->
    $scope.location = $location


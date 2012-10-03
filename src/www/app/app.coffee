'use strict'

# gpsModule = angular.module 'gpsModule', ['map', 'todo', 'LogModule']

gpsModule = angular.module 'gpsModule', ['map', 'log', 'ui', 'config', 'api']


gpsModule.controller "navigationCtrl", [
    "$scope"
    "$location"
    "Account"
($scope, $location, Account) ->
    $scope.location = $location
]

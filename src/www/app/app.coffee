'use strict'

# gpsModule = angular.module 'gpsModule', ['map', 'todo', 'LogModule']

gpsModule = angular.module 'gpsModule', ['map', 'log', 'ui', 'config', 'api']

"""
gpsModule.config ($routeProvider) ->
    log 'gpsModule.config ($routeProvider)', $routeProvider
    $routeProvider.when '/log/:skey', {
        #templateUrl: '',
        #controller: 'logControl'
    }
"""

gpsModule.controller "navigationCtrl", [
    "$scope"
    "$rootScope"
    "$location"
    "Account"
($scope, $rootScope, $location, Account) ->
    log 'navigationCtrl:', $scope
    $scope.location = $location
    #$scope.connected = $rootScope.connect.connected
]

gpsModule.directive 'navUrl', [
    "$rootScope"
    ($rootScope) -> {
        restrict: 'A'
        link: (scope, element, attrs) ->
            #ngPopupUrl = attrs['ngPopupUrl']
            navUrl = attrs['navUrl'] or 'blank'
            $rootScope.navurl = $rootScope.navurl or {}
            $rootScope.navurl[navUrl] = element
            #log ':: nav-url = ', navUrl, attrs, scope, $rootScope
        #controller: ($scope) ->
    }
]

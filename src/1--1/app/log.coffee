'use strict'

LogModule = angular.module 'log', ['ngResource', 'ui', 'systems']
#log 'LogModule=', LogModule

LogModule.controller "logControl", [
    "$scope", "$rootScope", ($scope, $rootScope) ->
        $scope.logs = [
            "1"
            "2"
            "3"
        ]
        $scope.more = () ->
            #$scope.show = !$scope.show
            log "TODO: Подгрузить записи...", $rootScope
            $scope.logs.push "3"
]

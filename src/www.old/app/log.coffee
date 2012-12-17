'use strict'

LogModule = angular.module 'log', ['ngResource', 'ui', 'systems']
#log 'LogModule=', LogModule

LogModule.config ($routeProvider) ->
    log 'LogModule.config ($routeProvider)', $routeProvider
    $routeProvider.when '/log', {}
    $routeProvider.when '/log/:skey', {}

LogModule.controller "logControl", [
    "$scope"
    "$rootScope"
    "$route"
    "$http"
($scope, $rootScope, $route, $http) ->
    #$scope.mylogs = new Logs
    #log '  logControl:$location:$routeParams = ', $location, $routeParams, $route
    #$scope.route = $route
    #$scope.params = $routeParams
    #$route.routes = {
    #    "/log/(:skey)"
    #}
    $scope.logs = []
    $scope.$on '$locationChangeSuccess', () ->
        log '$locationChangeSuccess(log) = ', $scope, $route
        if not $route.current
            return
        newkey = $route.current.params.skey
        if $scope.skey == newkey
            return

        $scope.skey = newkey
        if $scope.skey
            $rootScope.navurl['/log'].attr 'href', '/#/log/' + $scope.skey
        else
            $rootScope.navurl['/log'].attr 'href', '/#/log'

        if not $scope.skey
            $scope.logs = []
            return

        $http.get('/api/logs/' + $scope.skey + "/" + (new Date()).getTime()).success( (data) ->
            $scope.logs = data.logs
        )

        #window.hhhh = $route

        #  $scope, $rootScope, typeof($location), typeof($route)
        #if $location.match(/\/map/)
        #    #log '==MAP'
        #    if config.map
        #        google.maps.event.trigger config.map, 'resize'

    $scope.dellog = (skey, lkey) ->
        if not skey
            return
        log 'onDel:', skey, lkey, $scope
        for l of $scope.logs
            if $scope.logs[l].lkey == lkey
                log 'found at', l
                #delete $scope.getlogs2(skey).logs[l]
                $scope.logs.splice l, 1
                $http.delete('/api/logs/' + $scope.skey + "/" + (new Date()).getTime()).success( (data) ->
                    #$scope.logs = data.logs
                    log 'delete done', data
                )

    $scope.on_select = () ->
        log 'on_select'

    $scope.more = () ->
        #$scope.show = !$scope.show
        log "TODO: Подгрузить записи...", $rootScope
        $scope.logs.push "3"

    #$scope.logs = new Logs

    $scope.dont_press = () ->
        #$scope.$root.api.$save()
        #a = new Account()
        #a.$save {a:1}
        #$scope.logs.$save({skey:1})
        log 'oh NOOOOOOOOOOO', $scope.$root
]

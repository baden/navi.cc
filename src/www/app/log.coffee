'use strict'

LogModule = angular.module 'log', ['ngResource', 'ui', 'systems']
#log 'LogModule=', LogModule

LogModule.factory "Logs2", ($resource) ->
    log 'Logs:constructor'
    $resource "/api/logs/:id/:action", {},
        create:
            method: "PUT"

        saveData:
            method: "POST"

        toggle:
            method: "GET"
            params:
                action: "toggle"

LogModule.factory "Logs", [
    "$resource",
    "$rootScope",
($resource, $rootScope) ->
    load = $resource "/api/logs/:skey", {}
    logs = $rootScope.logs = {}
    '''
    i = 0
    while i < loadList.length
        data[loadList[i]] = load.get(name: loadList[i])
        i++
    '''
    return (skey) ->
        log '   get Logs by skey:', skey, load, logs, $rootScope
        if not skey
            return []
        if not logs[skey]
            #logs[skey] = load.get {skey: skey}
            logs[skey] = []
            for i in [1..100]
                logs[skey].push {
                    lkey: skey
                    dt: i
                    text: "Hello " + skey
                }
        logs[skey]
]

LogModule.controller "logControl", [
    "$scope"
    "$rootScope"
    "Logs"
($scope, $rootScope, Logs) ->
    #$scope.mylogs = new Logs
    $scope.logs = [
        "1"
        "2"
        "3"
    ]
    $scope.getlogs = (key) -> Logs(key)
    log '    $scope.getlogs =', $scope.getlogs, Logs
    $scope.getlogs2 = (syskey) ->
        [
            "1"
            syskey
            "3"
        ]
    $scope.on_select = () ->
        log 'on_select'

    $scope.more = () ->
        #$scope.show = !$scope.show
        log "TODO: Подгрузить записи...", $rootScope
        $scope.logs.push "3"

    $scope.logs = new Logs

    $scope.dont_press = () ->
        #$scope.$root.api.$save()
        #a = new Account()
        #a.$save {a:1}
        $scope.logs.$save({skey:1})
        log 'oh NOOOOOOOOOOO', $scope.$root
]

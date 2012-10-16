# Все что касается списка систем
# Работа с API

'use strict'
SystemsModule = angular.module 'systems', ['ngResource', 'ui', 'api', 'connect']

#Array::remove = (e) -> @[t..t] = [] if (t = @indexOf(e)) > -1

SystemsModule.factory 'Systems', ["$rootScope", ($rootScope) ->
    data = {
        systems: []
    }
    addRandomMarker = ->
        #console.log 'tick', data
        $rootScope.$apply ->
            for k, v of data.systems
                #log 'k, v=', k, v
                if v.last
                    #console.log v.last.point
                    v.last.point.lat += 0.001 * (Math.random()-0.5)
                    v.last.point.lon += 0.001 * (Math.random()-0.5)
        #    data.systems.push new google.maps.LatLng(48.5, 34.5)

    setInterval ( () ->
        addRandomMarker()
    ), 100

    return data
]

SystemsModule.run ["$rootScope", "Account", "Connect", "Systems", ($rootScope, Account, Connect, Systems) ->
    #log 'SystemsModule.run', $rootScope, Account

    $rootScope.api = Account.get( (d)->
        log 'done', d
        #Systems.systems .push new google.maps.LatLng(48.6, 34.5)
        Systems.systems = $rootScope.api.account.systems
        $rootScope.$watch "api.account.systems", ( (d)->
            skeys = $rootScope.api.account.sys_keys
            newskeys = []
            for s in skeys
                if s of d
                    newskeys.push s
            $rootScope.api.account.sys_keys = newskeys
            #log '$watch $rootScope.api.account.systems triggered', d
            Connect.send {
                akey: 'me'
                message: 'syspurge'
            }
        ), true
        $rootScope.$watch "api.account.sys_keys", ( (d)->
            #log '$watch $rootScope.api.account.sys_keys triggered', d
            Connect.send {
                akey: 'me'
                message: 'syspurge'
            }
        ), true
        # Нужно попробовать и обратную watch
    )
    #$rootScope.systems = $rootScope.api.account.systems

    log '$rootScope.account=', $rootScope.account
]

SystemsModule.filter 'bytags', () ->
    (array, tags, end) ->
        #log 'bytags:filter', array, tags, end
        if !tags
            return array
        out = {}
        for i of array
            #log 'i=', i, array[i]
            if tags.length == 0
                out[i] = array[i]
            else:
                for k in tags
                    #log 'k=', k
                    if k in array[i].tags
                        out[i] = array[i]
                        break
        return out

SystemsModule.filter 'bytag', () ->
    (array, tag, end) ->
        #log 'bytag:filter', array, tag, end
        if !tag
            return array
        out = {}
        for i of array
            #log 'i=', i, array[i]
            if tag in array[i].tags
                out[i] = array[i]
        return out

SystemsModule.directive 'sysselect', () ->
    {
        restrict: 'E'
        replace: true
        transclude: true
        template: '
        <span>
            <select ng-model="selecttag">
                <option value="" selected>Все</option>
                <option value="{{t}}" ng-repeat="t in systems.tags" > {{ t }}</option>
            </select>
            <select ONCHANGE="location = this.options[this.selectedIndex].value;" value="/#{{preurl}}">
                <option value="/#{{preurl}}" selected="1">Выберите</option>
                <option value="/#{{preurl}}/{{a}}" ng-repeat="a in $root.api.account.sys_keys">
                    {{ $index }}:{{ $root.api.account.systems[a].desc }}
                </option>
            </select>
            {{ selecttag }}
        </span>'
        link: ($scope, element, attrs) ->
            $scope.on_select = attrs["ngSelectionChange"]
            $scope.preurl = attrs["preUrl"]
            log 'sysselect:link', $scope, element, attrs

        controller: ["$scope", "$rootScope", ($scope, $rootScope) ->
            $scope.systems = $rootScope.systems
            #$scope.selecttag = "1"
            $scope.on_select = () ->
                log 'on_select'
            $scope.hide = () ->
                log 'hide me'
        ]
    }


SystemsModule.controller "sysselect", ["$scope", "$rootScope", ($scope, $rootScope) ->
    #log "controller:sysselect"
    $scope.systems = $rootScope.systems
    #$scope.selecttag = "1"
    $scope.hide = () ->
        log 'hide me'
]

# Все что касается списка систем
# Работа с API

'use strict'
SystemsModule = angular.module 'systems', ['ngResource', 'ui', 'api']

#Array::remove = (e) -> @[t..t] = [] if (t = @indexOf(e)) > -1

SystemsModule.run ["$rootScope", "Account", ($rootScope, Account) ->
    log 'SystemsModule.run', $rootScope, Account

    $rootScope.api = Account.get( (d)->
        log 'done', d
        $rootScope.$watch "api.account.systems", ( (d)->
            skeys = $rootScope.api.account.sys_keys
            newskeys = []
            for s in skeys
                if s of d
                    newskeys.push s
            $rootScope.api.account.sys_keys = newskeys
            log '$watch $rootScope.api.account.systems triggered', d
        ), true
        $rootScope.$watch "api.account.sys_keys", ( (d)->
            log '$watch $rootScope.api.account.sys_keys triggered', d
        ), true
        # Нужно попробовать и обратную watch
    )
    #$rootScope.systems = $rootScope.api.account.systems

    log '$rootScope.account=', $rootScope.account
    '''
    $rootScope.systems = {
        list: {
            "12sdsder": {
                tags: ["все", "личные"]
                name: "Автомобиль 2"
                imei: "123456789012345"
                phone: "+380679332332"
            }
            "14sdsder": {
                tags: ["все", "служебные"]
                name: "Автомобиль 2"
                imei: "123456789012346"
                phone: "+380679332332"
            }
        }
        skeys: []
        defaulttag: "все"
        tags: [
            "все"
            "личные"
            "служебные"
            "партнеры"
            "перевозка"
        ]
    }
    for p in [1..20]
        $rootScope.systems.list["123" + p] = {
            tags: [$rootScope.systems.tags[p % 5]]
            name: "Автомобиль " + p
            imei: "123456789012345" + p
            phone: "+380679332332"
        }
    '''
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
            <select ng-model="selectsys" ng-selection-change="{{on_select}}">
                <!--option value="{{a.name}}" ng-repeat="a in systems.list | bytag:selecttag" ng-selected="$index == 0"-->
                <option value="{{a.name}}" ng-repeat="a in $root.api.account.sys_keys" ng-selected="$index == 0">
                    {{ $index }}:{{ $root.api.account.systems[a].desc }}
                </option>
            </select>
            {{ selecttag }}
            <ul>
            <li ng-repeat="s in systems.list | bytag:selecttag">{{ s }}</li>
            </ul>
        </span>'
        link: ($scope, element, attrs) ->
            $scope.on_select = attrs["ngSelectionChange"]
            log 'sysselect:link', $scope, element, attrs
            window.hhhh = attrs

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

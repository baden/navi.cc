# Все что касается списка систем
# Работа с API

'use strict'
SystemsModule = angular.module 'systems', ['ngResource', 'ui']

SystemsModule.run ["$rootScope", ($rootScope) ->
    #log 'SystemsModule.run', $rootScope

    $rootScope.systems = {
        list: {
            "12sdsder": {
                tags: ["все", "личные"]
                name: "Автомобиль 1"
            }
            "14sdsder": {
                tags: ["все", "служебные"]
                name: "Автомобиль 2"
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
        }
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
            <select ng-model="selectsys">
                <option value="{{a.name}}" ng-repeat="a in systems.list | bytag:selecttag" ng-selected="$index == 0">
                    {{ a.name }}:{{ a.tags }}:{{ $index }}
                </option>
            </select>
            {{ selecttag }}
            <ul>
            <li ng-repeat="s in systems.list | bytag:selecttag">{{ s }}</li>
            </ul>
        </span>'
        #link: ($scope, element, attrs, controller) ->
        #    log 'sysselect:link', $scope, element, attrs, controller

        controller: ["$scope", "$rootScope", ($scope, $rootScope) ->
            $scope.systems = $rootScope.systems
            #$scope.selecttag = "1"
            $scope.hide = () ->
                log 'hide me'
        ]
    }


SystemsModule.controller "sysselect", ["$scope", "$rootScope", ($scope, $rootScope) ->
    log "controller:sysselect"
    $scope.systems = $rootScope.systems
    #$scope.selecttag = "1"
    $scope.hide = () ->
        log 'hide me'
]

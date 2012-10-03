'''
sayHello = (name) -> "Hi, #{name}."
console.log(sayHello("BaDen "))

class Animal
    constructor: (name) ->
        @name = name
        console.log("Animal:constructor", name)

    run: ->
        console.log("Animal:run", @name)

animal = new Animal "dog"
animal2 = Animal("cat")
console.log "animal", animal
console.log "animal2", animal2
animal run
animal2 run
'''
myModule = angular.module("myModule", ["config", "logs"])
#log 'myModule'

'''
myModule.factory 'mySharedService', ["$rootScope", (rootScope) ->
    sharedService = {
        message: '123'
        broadcast: (@message) ->
            rootScope.$broadcast 'handleBroadcast'
    }
    sharedService
]
'''

myModule.controller "ControllerOne", [
    "$scope"
    "configShared"
    (scope, configShared) ->
        console.log "configShared", configShared
        scope.handleClick = (msg) ->
            configShared.broadcast(msg)

        scope.$on 'handleBroadcast', ->
            scope.message = configShared.message
]

myModule.controller "ControllerTwo", [
    "$scope"
    "configShared"
    (scope, configShared) ->
        scope.$on 'handleBroadcast', ->
            scope.message = configShared.message
]

myModule.controller "ControllerThree", [
    "$scope"
    "configShared"
    (scope, configShared) ->
        scope.$on 'handleBroadcast', ->
            scope.message = configShared.message
]



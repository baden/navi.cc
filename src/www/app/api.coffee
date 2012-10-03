apiModule = angular.module("api", ["ngResource"])

log 'apiModule=', apiModule

apiModule.factory 'Account', ["$resource", "$rootScope", ($resource, $rootScope) ->
    #return resource 'http://vpsua.navi.cc/api/logs/:id/:action', {}, {
    """
    $resource '/api/logs/:id/:action', {}, {
        '''
        create: { method: 'PUT' }
        saveData: { method: 'POST' }
        toggle: { method:'GET', params: {action: 'toggle'} }
        '''
    }
    """
    $rootScope.$watch "Account", (->
        log '$watch Account'
    ), true

    #$resource '/api/account/:userId', {userId:'@id'}
    $resource '/api/account/info.js', {userId:'@id'}
]


apiModule.run ["$rootScope", ($rootScope) ->
    log 'apiModule.run', $rootScope
]

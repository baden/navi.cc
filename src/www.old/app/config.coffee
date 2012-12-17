config = angular.module("config", ['popup.service', 'api'])
#log 'config'

###
    Это будет главный регистр с данными
###

config.factory 'configShared', ["$rootScope", (rootScope) ->
    configShared = {
        message: '123'
        map: null
        broadcast: (@message) ->
            rootScope.$broadcast 'handleBroadcast'
    }
    #console.log "configShared:constructor"
    configShared
]

#console.log "init:config", config
# Работа с событиями

logs = angular.module("logs", ["ngResource"])
#console.log "init:logs", logs
'''
myServices.factory('Entity', ['$resource', function ($resource) {
     return $resource('/api/entities', {}, {
     });
 }]);
'''
logs.factory 'Logs', ["$resource", ($resource) ->
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
    $resource '/api/log/:userId', {userId:'@id'}
]

logs.controller "logs", [
    "$scope"
    "configShared"
    "Logs"
    ($scope, configShared, Logs) ->
        console.log "logs:configShared", configShared
        console.log "logs:Logs", Logs
        $scope.logs = Logs.get {userId: 123}

        $scope.handleClick = (msg) ->
            configShared.broadcast(msg)

        $scope.$on 'handleBroadcast', ->
            scope.message = configShared.message
]



logs.directive 'logs', () ->
    restrict: 'E'
    transclude: true
    scope: {}
    template: '<div><h3>События</h3></div>'
    replace: true
    controller: [
        "$scope"
        "$element"
        "Logs"
        "$resource"
        ($scope, $element, Logs, $resource) ->
            window.User = User = $resource '/api/user/:userId', {userId:'@id'}
        '''
        console.log "User", User
        console.dir User
        user = User.get {userId: 123}, () ->
            console.log "user", user
            user.abc = true;
            user.$save();
        '''

        #$scope.config = config;
        # var api = new serverApp();
        $scope.logs = Logs.get {userId: 123}
        console.log 'logs: controller', $scope
    ]
    link: ["$scope", "$element", "attrs", ($scope, $element, attrs) ->
        console.log 'attrs=', attrs
        console.log 'name=', attrs.name
    ]

config.directive 'ngAlert', (PopupService) ->
    {
        restrict: 'E'
        link: (scope, element, attrs) ->
            # Could have custom or boostrap modal options here
            popupOptions = {}
            element.bind "click", () ->
                PopupService.alert(attrs["title"], attrs["text"],
                        attrs["buttonText"], attrs["alertFunction"],
                        scope, popupOptions)
        controller: ($scope) ->
            $scope.okay = () ->
                log 'okay'
                PopupService.close()
    }

config.directive 'ngConfirm', (PopupService) ->
    {
        restrict: 'E'
        link: (scope, element, attrs) ->
            # Could have custom or boostrap modal options here
            #log 'ngConfirm', scope
            popupOptions = {}
            element.bind "click", () ->
                PopupService.confirm(attrs["title"], attrs["actionText"],
                        attrs["actionButtonText"], attrs["actionFunction"],
                        attrs["cancelButtonText"], attrs["cancelFunction"],
                        scope, popupOptions);
        controller: ($scope) ->
            $scope.yes = () ->
                log 'yes'
                PopupService.close()
            $scope.no = () ->
                log 'no'
                PopupService.close()
    }

#window.hhh = []
#config.directive 'ngPopup', (PopupService) ->
config.directive 'ngAddSystem', (PopupService) ->
    {
        restrict: 'A'
        scope: true  # Это для того, чтобы для каждого элемента создавался новый scope
        link: (scope, element, attrs) ->
            scope.me = element
            #window.hhh.push(scope)
            #log 'scope.me=', scope.me
            #log 'ngAddSystem=', scope, element, attrs
        controller: ($scope) ->
            $scope.add_system_add = () ->
                #log 'add_system_add'
                #log 'scope.me=', $scope.me
                #PopupService.close()
                $scope.me.modal 'hide'
            $scope.add_system_cancel = () ->
                #log 'cancel'
                #log 'scope.me=', $scope.me
                $scope.me.modal 'hide'
                #PopupService.close()
    }

config.directive 'ngSortable', (PopupService) ->
    {
        restrict: 'A'
        link: (scope, element, attrs) ->
            #log 'ngSortable:link', scope, element, attrs
            element.sortable({
                handle: '.msp'
                revert: true
                scrollSpeed: 5
                #delay: 200
                #placeholder: 'ui-state-highlight'
                placeholder: 'ui-sortable-placeholder2'
                cursor: 'crosshair'
                #'revert': 2000
                #axis: "y"
                stop: (event, ui)->
                    #log 'do sort', event, ui, element, scope, element.find('li')
                    nslist = [].map.call(
                        element.find('li'), (el) ->
                            return el.dataset.skey
                    )
                    #log '  nslist=', nslist
                    #scope.$broadcast 'sort', nslist
                    scope.$root.api.account.sys_keys = nslist
                    scope.$apply()

                    #for e in element
            })
    }
"""
["$scope", (scope) ->
    console.log 'add_system', scope
    scope.add_system_add = (el) ->
        console.log 'add', scope, el
    scope.add_system_cancel = (el) ->
        console.log 'cancel', scope, el
]
"""

#var directivesModule = angular.module('popup.directives', []);
config.directive 'ngPopup', (PopupService) ->
    {
        restrict: 'A'
        link: (scope, element, attrs) ->
            #ngPopupUrl = attrs['ngPopupUrl']
            ngPopup = attrs['ngPopup']
            #log 'ngPopup=', ngPopup, attrs
            # Could have custom or boostrap modal options here
            popupOptions = {}
            element.bind "click", () ->
                PopupService.dialog ngPopup, scope, popupOptions
        controller: ($scope) ->
            $scope.doIt = () ->
                #log 'doIt'
                PopupService.close()
            $scope.cancel = () ->
                #log 'cancel'
                PopupService.close()
    }

config.directive 'ngPopupUrl', (PopupService) ->
    {
        restrict: 'A'
        link: (scope, element, attrs) ->
            ngPopupUrl = attrs['ngPopupUrl']
            # Could have custom or boostrap modal options here
            popupOptions = {}
            element.bind "click", () ->
                PopupService.load ngPopupUrl, scope, popupOptions
        controller: ($scope) ->
            $scope.doIt = () ->
                #log 'doIt'
                PopupService.close()
            $scope.cancel = () ->
                #log 'cancel'
                PopupService.close()
    }

servicesModule = angular.module 'popup.service', []
servicesModule.factory 'PopupService', ($http, $compile) ->
    popupService = {}

    popupService.getPopupById = (id) ->
        popupService.popupElement = $('#' + id)
        if popupService.popupElement.size() == 0
            popupService.popupElement = $( '<div id="' + id + '" class="modal hide"></div>' )
            popupService.popupElement.appendTo 'BODY'
        popupService.popupElement

    popupService.getPopup = () ->
        popupService.popupElement

    ###
    popupService.getPopup = (create) ->
        if !popupService.popupElement and create
            popupService.popupElement = $( '<div class="modal hide"></div>' )
            popupService.popupElement.appendTo 'BODY'

        popupService.popupElement
    ###
    popupService.compileAndRunPopup = (popup, scope, options) ->
        $compile(popup) scope
        popup.modal options

    popupService.alert = (title, text, buttonText, alertFunction, scope, options) ->
        text = text ? text : "Alert"
        buttonText = buttonText ? buttonText : "Ok"
        alertHTML = ""
        if title
            alertHTML += "<div class=\"modal-header\"><h1>#{title}</h1></div>"
        alertHTML += "<div class=\"modal-body\">#{text}</div><div class=\"modal-footer\">"
        if alertFunction
            alertHTML += "<button class=\"btn\" ng-click=\"#{alertFunction}\">#{buttonText}</button>"
        else
            alertHTML += "<button class=\"btn\">#{buttonText}</button>"
        alertHTML += "</div>"
        popup = popupService.getPopupById "popup_modal", true
        popup.html alertHTML
        if !alertFunction
            popup.find(".btn").click () ->
                popupService.close()

        popupService.compileAndRunPopup popup, scope, options

    # Is it ok to have the html here? should all this go in the directives? Is there another way
    # get the html out of here?
    popupService.confirm = (title, actionText, actionButtonText, actionFunction, cancelButtonText, cancelFunction, scope, options) ->
        actionText = actionText ? actionText : "Are you sure?"
        actionButtonText = actionButtonText ? actionButtonText : "Ok"
        cancelButtonText = cancelButtonText ? cancelButtonText : "Cancel"

        popup = popupService.getPopupById "popup_modal", true
        confirmHTML = ""
        if title
            confirmHTML += "<div class=\"modal-header\"><h1>#{title}</h1></div>"
        confirmHTML += "<div class=\"modal-body\">#{actionText}</div><div class=\"modal-footer\">"
        if actionFunction
            confirmHTML += "<button class=\"btn btn-primary\" ng-click=\"#{actionFunction}\">#{actionButtonText}</button>"
        else
            confirmHTML += "<button class=\"btn btn-primary\">#{actionButtonText}</button>"
        if cancelFunction
            confirmHTML += "<button class=\"btn btn-cancel\" ng-click=\"#{cancelFunction}\">#{cancelButtonText}</button>"
        else
            confirmHTML += "<button class=\"btn btn-cancel\">#{cancelButtonText}</button>"
        confirmHTML += "</div>"
        popup.html confirmHTML
        if !actionFunction
            popup.find(".btn-primary").click () ->
                popupService.close()
        if !cancelFunction
            popup.find(".btn-cancel").click () ->
                popupService.close()
        popupService.compileAndRunPopup popup, scope, options

    popupService.dialog = (id, scope, options) ->
        #popup = popupService.getPopup true
        popup = popupService.getPopupById id
        log 'popup', popup
        popup.modal options
        # Tried getting this to work with the echo and a post, with no luck, but this gives you the idea
        # popup.html(data);
        #popup.html htmlPage
        #popupService.compileAndRunPopup popup, scope, options

    popupService.load = (url, scope, options) ->
        htmlPage = '
            <div class="modal-header">
                <h1>Header</h1>
            </div>
            <div class="modal-body">
                Body
            </div>
            <div class="modal-footer">
                <button class="btn btn-primary" ng-click="doIt()">
                    Do it
                </button>
                <button class="btn btn-cancel" ng-click="cancel()">
                    Cancel
                </button>
            </div>'

        $http.get(url).success (data) ->
            popup = popupService.getPopup true
            # Tried getting this to work with the echo and a post, with no luck, but this gives you the idea
            # popup.html(data);
            popup.html htmlPage
            popupService.compileAndRunPopup popup, scope, options

    popupService.close = () ->
        console.log('popupService.close')
        popup = popupService.getPopup()
        if popup
            popup.modal 'hide'
    popupService

config.controller 'SysConfig', ["$scope", "PopupService", ($scope, PopupService) ->
    $scope.del = (el) ->
        #skey = @.a
        #index = @.$index
        #log 'del', el, skey, index, $scope
        #log 'sys_key', $scope.$root.api.account.sys_keys[index]
        #log 'system', $scope.$root.api.account.systems[skey]

        delete $scope.$root.api.account.systems[el]

    $scope.tags = (el) ->
        log 'setTag'

    $scope.icon = (el) ->
        log 'setIcon'

    $scope.edit = (el) ->
        log 'edit', el
        popupOptions = {}
        $scope.$parent.current = $scope.$root.api.account.systems[el]
        PopupService.dialog "config_edit_system", $scope, popupOptions

    $scope.onoff = (el) ->
        log 'setOnOff'

    $scope.yes = (el) ->
        log 'yes reload', el, $scope
        $scope.del(el)
        $scope.$parent.okay()
        #popupService.close()

    $scope.$on 'sort', (p, sys_list)->
        #scope.message = configShared.message
        log 'new sort', p, sys_list, $scope
        $scope.$root.api.account.sys_keys = sys_list
        # TODO: Кажется это не гарантирует перехват изменений
        #angular.apply()
        $scope.$apply() # TODO: Нахрена спрашивается я извращался с $on если оно само не отслеживает

    $scope.sort = (new_syslist) ->
        log 'new sort'
]
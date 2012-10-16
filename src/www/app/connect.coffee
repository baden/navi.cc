# Работа полнодуплексного соединения

connectModule = angular.module("connect", [])

log 'connectModule=', connectModule

connectModule.factory 'Connect', ["$rootScope", ($rootScope) ->
    sendData = {
        message: ''
        send: (msg) ->
            @message = msg
            @broadcast()
        broadcast: () ->
            $rootScope.$broadcast 'channel_send'
    }

    return sendData
]

connectModule.run ["$rootScope", "Connect", ($rootScope, Connect) ->
    #log 'apiModule.run', $rootScope
    #$rootScope.connect = new Connection 'http://localhost:8281/chat'
    #$rootScope.sock = sock = null
    $rootScope.connect = {
        connected: false
        sock: null
        comment: "Инициализация..."
    }

    connect = (timeout) ->
        timeout = 60 if timeout > 60
        console.log 'connecting to http://localhost:8281/chat...'
        $rootScope.connect.sock = sock =  new SockJS 'http://localhost:8281/chat'
        sock.onopen = () ->
            console.log 'Connect:open'
            $rootScope.connect.connected = true
            $rootScope.connect.comment = "Соединение с сервером установлено."
            $rootScope.$apply()
            timeout = 1

        sock.onmessage = (e) ->
            console.log 'Connect:message', e.data

        sock.onclose = () ->
            console.log "Connect:close. reconnect after #{timeout} sec"
            $rootScope.connect.connected = false
            $rootScope.connect.comment = "Утеряно соединение с сервером.\nПовторная попытка через несколько секунд."
            $rootScope.$apply()
            setTimeout ( () ->
                connect(timeout*2)
            ), timeout*1000
    connect(1)

    $rootScope.$on 'channel_send', (e) ->
        message = Connect.message
        #log 'on:channel_send', message
        #scope.message = configShared.message
]

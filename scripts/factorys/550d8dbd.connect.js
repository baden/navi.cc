wwwGPSApp.factory('Connect', ["$rootScope", function($rootScope) {
    var shared = {};
    shared.updater = {};
    shared.updater.queue = {};

    shared.updater.on = function(msg, foo){
        shared.updater.queue[msg] = shared.updater.queue[msg] || [];
        shared.updater.queue[msg].push(foo);
    };

    shared.updater.process = function(msg){
        var i;
        if(shared.updater.queue[msg.message]){
            for(i in shared.updater.queue[msg.message]){
                shared.updater.queue[msg.message][i](msg);
            }
        }
        if(shared.updater.queue['*']){
            for(i in shared.updater.queue['*']){
                shared.updater.queue['*'][i](msg);
            }
        }
    };

    console.log("===> Connect:init");


    //var ws_server = "ws://gpsapi04.navi.cc:8888/socket";
    var ws_server = "http://gpsapi04.navi.cc:8888/socket";

    var connect = function(timeout){
        if(timeout>60) timeout = 60;
        console.log('connecting to ' + ws_server + '...');

        //new SockJS(ws_server)
        //var ws = $rootScope.ws = new WebSocket(ws_server);
        var ws = $rootScope.ws = new SockJS(ws_server);
        ws.onopen = function () {
            console.log('WebSocket connected');
            //$('#main').append('<div>Opened</div>');
            //ws.send("First msg");
        };
        ws.onmessage = function(event) {
            console.log('onmessage:', event.data);
            var msg = JSON.parse(event.data);
            //msg.map(function f(m){ shared.updater.process(m); });
            shared.updater.process(msg);
            //shared.send(event.data);
            //$rootScope.$broadcast('channel_data', event.data);
            //$rootScope.$broadcast('change_last');
            //$('#main').append('<div>' + event.data + '</div>');
        };
        ws.onclose = function(event) {
            console.log('WebSocket disconnected');
            setTimeout(function(){
                connect(timeout*2);
            }, timeout*1000);
        };
    };
    connect(1);

    shared.message = '';

    shared.send = function(msg) {
        this.message = msg;
        //this.broadcastItem();
        $rootScope.$broadcast('channel_data', 'aaa');
    };

    /*sharedService.broadcastItem = function() {
        $rootScope.$broadcast('channel_data');
    };*/

    return shared;
}]);


"use strict";

(function(window, SockJS) {

//window.config = window.config || {};
var console = window.console;
var config = window.config;

// Система автообновления
config.updater = {};
config.updater.queue = {};

config.updater.add = function(msg, foo){
    config.updater.queue[msg] = config.updater.queue[msg] || [];
    config.updater.queue[msg].push(foo);
};

config.updater.process = function(msg){
    var i;
    if(config.updater.queue[msg.message]){
        for(i in config.updater.queue[msg.message]){
            config.updater.queue[msg.message][i](msg);
        }
    }
    if(config.updater.queue['*']){
        for(i in config.updater.queue['*']){
            config.updater.queue['*'][i](msg);
        }
    }
};

config.updater.add('*', function(msg){
    console.log("Channel: onMessage", msg);
    //console.log(msg);
    //log('goog.appengine.Channel: onMessage:', msg);
    //connected = true;
/*
    if(config.admin){
        //if(msg.msg) message('Получено сообщени об обновлении:<b>' + msg.msg + '</b>');
        if(msg.msg) log('Получено сообщение от сервера:<b>', msg);
    }
*/
});

config.updater.add('change_icon', function(msg) {
    config.account.systems[msg.skey].icon = msg.data.name;
});

config.updater.tabs = [];

//window['Updater'] = Updater;

// Установим chanel-соединение
// Получим токен для установки соединения
var uuid = (new Date()).getTime().toString(36) + Math.floor(Math.random() * 2147483648).toString(36);
var connect = function(timeout){
    if(timeout>60) timeout = 60;
    console.log('connecting to ' + ws_server + '...');

    //new SockJS(ws_server)
    //var ws = $rootScope.ws = new WebSocket(ws_server);
    //var ws_server = "http://gpsapi04.navi.cc:8888/socket";
    var ws_server = "http://localhost:8888/socket";

    var ws = new SockJS(ws_server);
    ws.onopen = function () {
        console.log('WebSocket connected');
        //$('#main').append('<div>Opened</div>');
        //ws.send("First msg");
    };
    ws.onmessage = function(event) {
        console.log('onmessage:', event.data);
        var msg = JSON.parse(event.data);
        //msg.map(function f(m){ config.updater.process(m); });
        config.updater.process(msg);
    };
    ws.onclose = function(event) {
        console.log('WebSocket disconnected');
        setTimeout(function(){
            connect(timeout*2);
        }, timeout*1000);
    };
};
connect(1);


})(window, SockJS);

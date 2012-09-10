// log.js

'use strict';

(function(window){

var LogModule = angular.module('LogModule', ['ngResource']).
    value('skey', {
        load: function(name) {
            this.name = name;
        }
    });

LogModule.factory('Log', function($resource){
    log('factory:Log');
    return $resource('emuapi/log/:skey.json', {}, {
        query: {
            method: 'GET',
            params:{
                skey: '0'
            },
            isArray: true
        }
    });
});

// Ставит перед числом нужное кол-во нулей чтобы длина записи была равна digits
var fdigits = function(value, digits) {
    return ("00000000000" + value).slice(-digits);
}

LogModule.filter('datetime', function(){
    return function(input){
        var timestamp = parseInt(input);
        var d = new Date(timestamp*1000);
        return '' + fdigits(d.getDate(),2) + '/' + fdigits(d.getMonth()+1, 2) + '/' + d.getFullYear() + ' ' +
            fdigits(d.getHours(), 2) + ':' + fdigits(d.getMinutes(), 2) + ':' + fdigits(d.getSeconds(), 2);
    }
});

LogModule.controller('logController', function($scope, skey, Log) {
    log('logController:', $scope, skey, Log);
    //$scope.logs = [];
    $scope.logs = window.config.logs = Log.query();
});

})(this);

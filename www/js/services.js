// services.js


angular.module('logServices', ['ngResource']).
    factory('Log2', function($resource){
        return $resource('api/log2/:skey.json', {}, {
            query: {
                method: 'GET',
                params:{
                    skey: 'skey'
                },
                isArray:true
            }
        });
    });

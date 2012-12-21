'use strict';

var wwwGPSApp = angular.module('wwwGPSApp', []);

//wwwGPSApp.value('abc', 'def');

/*wwwGPSApp.factory('account', ["$resource", function($resource){
  //console.log('Loading account data', $resource);
  return $resource('http://new.navi.cc/api/account/info.js&id=:id', {id:"@id"}, {
  });
}]);
*/

/*wwwGPSApp.service('abc', function($http){
  console.log('calculation of abc', $http);
  this.name = 'def';
});*/




wwwGPSApp.run(["$rootScope", "$http", function($rootScope, $http){
  $rootScope.account = []
  $http.get("http://new.navi.cc:7080/api/account/info.js").success(function(data){
    $rootScope.account = data;
  });
  console.log("wwwGPSApp:run", $rootScope);

}]);


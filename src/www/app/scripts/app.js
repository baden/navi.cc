'use strict';

var apiserver = "http://localhost:8183";

angular.module('resources.account', []);
angular.module('resources.account').factory('Account', ['$http', function ($http) {
  console.log('-- resources.account.Account');
  var akey = localStorage.getItem('akey');
  var akey = localStorage.getItem('akey');
  var Account = {
    'name': 'noname-noface-nonumber',
    'akey': akey,
    'account': null
  };

  if(akey){
    $http.get(apiserver + "/api/account/get?akey=" + akey).success(function(data){
      console.log('login data=', data);
      if(data.account) Account.account = data.account;
    });
  }

  //$scope.akey = akey;

  return Account;
}]);


angular.module('resources.systems', ['resources.account']);
angular.module('resources.systems').factory('Systems', ['Account', function (Account) {
  console.log('-- resources.systems.Systems', Account, Account.akey);
  var Systems = {
    account: Account,
  };
  Systems.all = function(){
    console.log('Systems.all');
    return [1,2,3];
  }
  return Systems;
}]);


angular.module('AccountPage', ['resources.account'], ['$routeProvider', function($routeProvider){
  $routeProvider.when('/', {
    templateUrl:'login.html',
    controller:'LoginCtrl',
    resolve:{
      account:['Account', function(Account){
        return Account;
      }]
    }
  });
}]);


angular.module('AccountPage').controller('LoginCtrl', ['$scope', 'account', '$http', function($scope, account, $http){
  console.log('AccountPage', $scope, account);
  $scope.account = account;
  $scope.loginform = false;
  $scope.hostname = location.hostname;


  $scope.onLogout = function(){
      localStorage.removeItem('akey');
      location.reload();
  };

  $scope.onLogin = function(){
    $scope.loginform = false;
    console.log('Login;', $scope);

    if(($scope.account.newusername === "")||(!$scope.account.newusername)) {
      return;
    }

    $http.get(apiserver + "/api/account/new?domain=" + encodeURIComponent(location.hostname) +
      "&user=" + encodeURIComponent($scope.account.newusername) +
      "&password=" + encodeURIComponent($scope.account.newpass)
    ).success(function(data){
      console.log('login data=', data);
      localStorage.setItem('akey', data.account.akey);
      if(data.result == "created") {
        $scope.label = "Создана новая учетная запись. Вход через 3 секунды.";
        setTimeout(function(){location.reload();}, 3000);
      } else {
        $scope.label = "Вход в учетную запись...";
        setTimeout(function(){location.reload();}, 1000);
      }


      //$rootScope.account = data;
    });

    return false;
  }
}]);


angular.module('MapPage', ['resources.account'], ['$routeProvider', function($routeProvider){
  $routeProvider.when('/map', {
    templateUrl:'map.html',
    controller:'MapCtrl',
    resolve:{
      account:['Account', function(Account){
        return Account;
      }]
    }
  });
}]);

angular.module('MapPage').controller('MapCtrl', ['$scope', 'account', function($scope, account){
  if(!account.akey){
    location = "/";
  }
  console.log('MapPage', $scope, account);
  $scope.account = account;
}]);


angular.module('LogPage', ['resources.systems'], ['$routeProvider', function($routeProvider){
  $routeProvider.when('/logs', {
    templateUrl:'logs.html',
    controller:'LogCtrl',
    resolve:{
      systems:['Systems', function(Systems){
        return Systems.all();
      }]
    }
  });
}]);

angular.module('LogPage').controller('LogCtrl', ['$scope', 'systems', function($scope, systems){
  console.log('LogPage', $scope, systems);
  $scope.systems = systems;
}]);




angular.module('ConfigPage', ['ui', 'resources.account'], ['$routeProvider', function($routeProvider){
  $routeProvider.when('/config', {
    templateUrl:'config.html',
    controller:'ConfigCtrl',
    resolve:{
      account:['Account', function(Account){
        return Account;
      }]
    }
  });
}]);

angular.module('ConfigPage').controller('ConfigCtrl', ['$scope', 'account', '$http', function($scope, account, $http){
  console.log('ConfigPage', $scope, account);
  if(!account.akey){
    location = "/";
  }
  $scope.deleteenable = false;
  $scope.addform = false;
  $scope.account = account;
  $scope.onAdd = function(imei){
    console.log('onAdd', imei, account);
    $http.get(apiserver + "/api/account/systems/add" +
      "?akey=" + encodeURIComponent($scope.account.akey) +
      "&imei=" + encodeURIComponent(imei)
    ).success(function(data){
      console.log('return data=', data);
      if(data.result == "already"){
        alert('Вы уже наблюдаете за этой системой.');
        return;
      }
      if(data.result == "notfound"){
        alert('Система на найдена. Возможные причины: \n1. Система еще не выходила на связь.\n2. Проверте правильность ввода IMEI.');
        return;
      }
      $scope.account.account.skeys.push(data.system.key);
      $scope.account.account.systems[data.system.key] = angular.copy(data.system);
      $scope.addform = false;
      //alert('Система ни разу не выходила на связь. Но она все равно была добавлена в список наблюдения.');
    });
  };
  $scope.onSort = function(){
    console.log('onSort');
    var payload = $.param({skeys:JSON.stringify($scope.account.account.skeys)});
    var config = {
      headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    };
    $http.post(apiserver + "/api/account/systems/sort" +
      "?akey=" + encodeURIComponent($scope.account.akey), payload, config
    ).success(function(data){
      console.log('return data=', data);
    });
  }
  $scope.onoff = function(el){
    $scope.account.account.systems[el].off = !$scope.account.account.systems[el].off;
    console.log('onoff', el);
  };
  $scope.del = function(el){
    //delete el;
    console.log('del', el);
    $http.get(apiserver + "/api/account/systems/del" +
      "?akey=" + encodeURIComponent($scope.account.akey) +
      "&skey=" + encodeURIComponent(el)
    ).success(function(data){
      console.log('return data=', data);
      var i = $scope.account.account.skeys.indexOf(el);
      $scope.account.account.skeys.splice(i, 1);
      delete $scope.account.account.systems[el];
    });
    //$scope.account.systems[]
  };
  var sortableEle = $('ul.config_sys_list').sortable({
    handle: ".msp",
    revert: true,
    scrollSpeed: 5,
    cursor: 'crosshair',
    placeholder: 'ui-sortable-placeholder2',
    stop: $scope.onSort
  });
  console.log("===", $('ul.config_sys_list'));
}]);



var wwwGPSApp = angular.module('wwwGPSApp', ['AccountPage', 'MapPage', 'LogPage', 'ConfigPage']);

wwwGPSApp.filter('datetime', function(){
    return function (text, length, end) {
        var d = new Date(parseInt(text, 10)*1000);
        return '' + fdigits(d.getDate(),2) + '/' + fdigits(d.getMonth()+1, 2) + '/' + d.getFullYear() + ' ' +
            fdigits(d.getHours(), 2) + ':' + fdigits(d.getMinutes(), 2) + ':' + fdigits(d.getSeconds(), 2);
    };
});

wwwGPSApp.filter('fromnow', function(){
    return function (text, length, end) {
        var d = new Date(parseInt(text, 10)*1000);
        return moment(parseInt(text, 10)*1000).fromNow();
    };
});

wwwGPSApp.filter('yesno', function(){
    return function (state, length, end) {
        return state?"да":"нет";
    };
});


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
  /*
  $http.get("http://new.navi.cc:7080/api/account/info.js").success(function(data){
    $rootScope.account = data;
  });
  */
  console.log("wwwGPSApp:run", $rootScope);

}]);


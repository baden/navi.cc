'use strict';

wwwGPSApp.controller('appCtrl', ["$scope", "$location", "Account", function($scope, $location, Account) {
    $scope.location = $location;
    $scope.account = Account;
    $scope.last_pos = {lan: 48.0, lon: 35.0};
    $scope.list = [
        'Встать',
        'Сделать',
        'Лечь спать'
    ];
    //$scope.account = account.get();
    for(var i=0; i<1; i++){
        $scope.list.push('Ollala');
    }
    $scope.doAdd = function(){
        $scope.list.push('править баги');
    };
    console.log("appCtrl", $scope, Account.akey);
}]);


wwwGPSApp.controller('appCtrl2', ["$scope", function($scope) {
  $scope.list = [
    'Другой',
    'список',
    'дел'
  ];
}]);

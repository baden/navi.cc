'use strict';

wwwGPSApp.controller('appCtrl', ["$scope", "$location", function($scope, $location) {
    $scope.location = $location;
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
    console.log("appCtrl", $scope);
}]);


wwwGPSApp.controller('appCtrl2', ["$scope", function($scope) {
  $scope.list = [
    'Другой',
    'список',
    'дел'
  ];
}]);

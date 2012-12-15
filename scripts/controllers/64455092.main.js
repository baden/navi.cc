'use strict';

wwwGPSApp.controller('appCtrl', ["$scope", "$location", function($scope, $location) {
    $scope.location = $location;
    $scope.list = [
        'Встать',
        'Сделать',
        'Лечь спать'
    ];
    console.log("appCtrl", $scope);
}]);


wwwGPSApp.controller('appCtrl2', ["$scope", function($scope) {
  $scope.list = [
    'Другой',
    'список',
    'дел'
  ];
}]);

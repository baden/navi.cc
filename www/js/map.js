// This is a module for cloud persistance in mongolab - https://mongolab.com
var MapModule = angular.module('map', ['ngResource']);
/*
  function initialize() {
        var latlng = new google.maps.LatLng(-34.397, 150.644);
        var myOptions = {
            zoom: 8,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
    var map = new google.maps.Map(document.getElementById("map_canvas"),
        myOptions);
  }*/
/*
MapModule.config(function($routeProvider) {
    log('MapModule:$routeProvider=', $routeProvider);
    $routeProvider.when('/map', {});
});
*/

MapModule.run(function($rootScope) {
    //log('MapModule.run', $rootScope);
    $rootScope.$on('$locationChangeSuccess', function($scope, $location, $route){
        //log('$locationChangeSuccess', $scope, $rootScope, typeof($location), typeof($route));
        if($location.match(/#\/map/)){
            //log('==MAP');
            if(config.map) {
                google.maps.event.trigger(config.map, 'resize');
            }
        }
    });
});


MapModule.directive('map', function(){
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        link: function($scope, element, attrs, controller){
            log('map:link', $scope, element, attrs, controller);
            var latlng = new google.maps.LatLng(48.497, 34.944);
            var myOptions = {
                    zoom: 11,
                    center: latlng,
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    //disableDefaultUI: true
                    overviewMapControl: true,
                    scaleControl: false,
                    rotateControl: false,
                    zoomControl: false,
                    streetViewControl: false,
                    panControl: false
            };
            config.map = new google.maps.Map(element[0],  myOptions);
        },
        template: '<div></div>',

        /*controller: function($scope, $route) {
            log('== MAP:controller', $scope, $route);
        }*/
        //templateUrl: 'templates/map.html'
    }
});

function MapCtrl($scope) {
  log('MapCtrl:start', $scope);
  initialize();
}

function LogsCtrl($scope) {
  log('LogsCtrl:start', $scope);
  //$scope.body =
}

function ReportCtrl($scope) {
  log('ReportCtrl:start', $scope);
}

//MapModule.controller =
/*
    factory('Project', function($resource) {
      var Project = $resource('https://api.mongolab.com/api/1/databases' +
          '/angularjs/collections/projects/:id',
          { apiKey: '4f847ad3e4b08a2eed5f3b54' }, {
            update: { method: 'PUT' }
          }
      );

      Project.prototype.update = function(cb) {
        return Project.update({id: this._id.$oid},
            angular.extend({}, this, {_id:undefined}), cb);
      };

      Project.prototype.destroy = function(cb) {
        return Project.remove({id: this._id.$oid}, cb);
      };

        log('map.init');
      return Project;
    });
*/

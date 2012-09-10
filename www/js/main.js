

var gl_scope;

// Глобальный регистр данных
window.config = {

}

var MainModule = angular.module('project', ['map', 'todo', 'LogModule']);

log('MainModule=', MainModule);

function navigationCtrl($scope, $location) {

  //required to high light the active navigational point
  $scope.location = $location;

}

MainModule.config(function($routeProvider) {
    log('$routeProvider=', $routeProvider);
    $routeProvider.
      when('/map', {controller:MapCtrl, templateUrl:'templates/map.html'}).
      when('/log', {controller:LogsCtrl, templateUrl:'templates/log.html'}).
      when('/report', {controller:ReportCtrl, templateUrl:'templates/report.html'}).
      otherwise({redirectTo:'/'});
  });

MainModule.controller('alog', function($scope) {
  $scope.map = 'hello';
  $scope.template = 'asdasdasdasd';
  log('alog', $scope);
});

// Я так понял что в angularjs пока нет обработки select. Поэтому реализуем самостоятельно:
MainModule.directive("ngSelectionChange", function( $compile ) {
        return function( $scope, $element, $attrs ) {
          //$element[0].onchange = function(e){
          jQuery( $element ).change( function( e ) {
              var target = jQuery( e.target );
              //var target = e.target;
              var actionKey = target.attr( "ng-selection-change" );
              var action = $scope.$eval( actionKey );
              var datasourceKey = target.attr( "ng-datasource" );
              var datasource = $scope.$eval( datasourceKey);
              var selectedIndex = target.prop( "selectedIndex" );
              var selectedItem = datasource[ selectedIndex ];

              action.call($scope, selectedItem);
          });
        }
      });

MainModule.directive('slist', function() {
  return {
    restrict: 'E',
    transclude: true,
    scope: {},
    controller: function($scope, $element) {
      $scope.selcat = 0;  // id выбранной категории
      var categories = $scope.categories = [
       {id: 0, title: 'все'},
       {id: 1, title: 'личные'},
       {id: 2, title: 'служебные'},
       {id: 3, title: 'партнеры'},
       {id: 4, title: 'ой, кто это?'},
      ];
      var slist = $scope.slist = [
        {title: 'Opel-Omega AE1856BE', categories:[0,1,2]},
        {title: 'Mercedes SL-300 AA0007AA', categories:[4]},
        {title: 'Очень длинное название автомобиля', categories:[2]},
        {title: '', hint:'Пустое название автомобиля', categories:[1]}
      ];
      $scope.select = function(s){
        log('slist:select', s);
          angular.forEach(slist, function(s) {s.selected = false;});
        s.selected = true;
      }
      $scope.change = function(c){
        log('slist:change', c.title);
        selcat = c.id;
      }
    },
    template:
      '<div class = "slist">'+
      '<select ng-datasource="categories" ng-selection-change="change">' +
        '<option ng-repeat="c in categories" ng-selected="c.id == selcat">{{ c.title }}</option>' +
      '</select>' +
      '<select ng-model="selectedItem" ng-options="i.title for i in categories">' +
        '<option value="">все</option>' +
      '</select>' +
      'Выбрано:{{selectedItem}}' +
      '<ul class="unstyled">' +
        '<li ng-repeat="s in slist" ng-class="{active:s.selected}" ng-click="select(s)" title="{{ s.hint }}">' +
          '<i class="icon-search"></i>' +
          '{{ s.title }}' +
        '</li>' +
      '</ul>' +
      '</div>',
    replace: true
  }
});


MainModule.directive('tabs', function() {
    return {
      restrict: 'E',
      transclude: true,
      scope: {},
      controller: function($scope, $element) {
        var panes = $scope.panes = [];

        $scope.select = function(pane) {
          angular.forEach(panes, function(pane) {
            pane.selected = false;
          });
          pane.selected = true;
        }

        this.addPane = function(pane) {
          if (panes.length == 0) $scope.select(pane);
          panes.push(pane);
        }
      },
      template:
        '<div class="tabbable">' +
          '<ul class="nav nav-tabs">' +
            '<li ng-repeat="pane in panes" ng-class="{active:pane.selected}">'+
              '<a href="" ng-click="select(pane)">{{pane.title}}</a>' +
            '</li>' +
          '</ul>' +
          '<div class="tab-content" ng-transclude></div>' +
        '</div>',
      replace: true
    };
  }).
  directive('pane', function() {
    return {
      require: '^tabs',
      restrict: 'E',
      transclude: true,
      scope: { title: '@' },
      link: function(scope, element, attrs, tabsCtrl) {
        tabsCtrl.addPane(scope);
      },
      template:
        '<div class="tab-pane" ng-class="{active: selected}" ng-transclude>' +
        '</div>',
      replace: true
    };
  });


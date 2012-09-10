// todo.js

var todoApp = {
    controller: {},
    directive: {}
}

todoApp.controller.TodoCtrl =  function($scope) {
  log('TodoCtrl:call', $scope);
  $scope.template = 'asdasdasdasd';
  $scope.todos = [
    {text:'learn angular', done:true},
    {text:'build an angular app', done:false}];

  //gl_scope = $scope.todos;
  //log(' == todos:', $scope.todos);

  $scope.addTodo = function() {
    $scope.todos.push({text:$scope.todoText, done:false});
    $scope.todoText = '';
  };

  $scope.remaining = function() {
    var count = 0;
    angular.forEach($scope.todos, function(todo) {
      count += todo.done ? 0 : 1;
    });
    return count;
  };

  $scope.archive = function() {
    var oldTodos = $scope.todos;
    $scope.todos = [];
    angular.forEach(oldTodos, function(todo) {
      if (!todo.done) $scope.todos.push(todo);
    });
  };
}

todoApp.directive.assa = function(){
    return {
        restrict: 'E',
        link: function($scope, element, attrs){
            log('assa:link', $scope, element, attrs);
        },
        template: '<div>ASSA</div>'
    }
}


angular.module('todo', []).
config(function($routeProvider) {
    //log('$routeProvider=', this);
    $routeProvider.
      when('/', {controller:todoApp.controller.TodoCtrl, templateUrl:'templates/todo.html'}).
      when('/todo', {controller:todoApp.controller.TodoCtrl, templateUrl:'templates/todo2.html'}).
      /*when('/edit/:projectId', {controller:EditCtrl, templateUrl:'detail.html'}).
      when('/new', {controller:CreateCtrl, templateUrl:'detail.html'}).*/
      otherwise({redirectTo:'/'});
  }).
      controller(todoApp.controller).
      directive(todoApp.directive);

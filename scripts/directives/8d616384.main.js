'use strict';

wwwGPSApp.directive('mylist', function() {
    return {
        restrict: 'E',
        //scope: {},
        transclude: false,
        template: '<div>List:<ul><li ng-repeat="l in list">{{ l }}</li></ul></div>',
        link: function(scope, element, attrs) {
            console.log('mylist directive: link', scope);
        }
    }
});

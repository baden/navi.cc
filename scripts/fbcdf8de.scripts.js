"use strict";var wwwGPSApp=angular.module("wwwGPSApp",[]);"use strict",wwwGPSApp.controller("appCtrl",["$scope","$location",function(a,b){a.location=b,a.list=["Встать","Сделать","Лечь спать"],console.log("appCtrl",a)}]),wwwGPSApp.controller("appCtrl2",["$scope",function(a){a.list=["Другой","список","дел"]}]),"use strict",wwwGPSApp.directive("mylist",function(){return{restrict:"E",transclude:!1,template:'<div>List:<ul><li ng-repeat="l in list">{{ l }}</li></ul></div>',link:function(a,b,c){console.log("mylist directive: link",a)}}});
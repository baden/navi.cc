"use strict";var wwwApp=angular.module("wwwApp",["lib"]).config(["$routeProvider",function(a){a.when("/",{templateUrl:"views/main.html",controller:"MainCtrl"}).otherwise({redirectTo:"/"})}]),lib=angular.module("lib",[]);console.log("hello, fromlib."),"use strict",wwwApp.controller("MainCtrl",["$scope",function(a){a.awesomeThings=["Верстаем сайт","Разрабатываем сервер","Ковыряемся в носу"]}]);
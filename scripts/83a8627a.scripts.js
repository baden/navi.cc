"use strict",function(a){a.log=function(){if(a.console)try{console.log(Array.prototype.slice.call(arguments))}catch(b){log("Error in console",b)}}}(window),"use strict";var wwwGPSApp=angular.module("wwwGPSApp",[]);wwwGPSApp.run(["$rootScope","$http",function(a,b){a.account=[],console.log("wwwGPSApp:run",a)}]),wwwGPSApp.factory("Connect",["$rootScope",function(a){var b={};b.updater={},b.updater.queue={},b.updater.on=function(a,c){b.updater.queue[a]=b.updater.queue[a]||[],b.updater.queue[a].push(c)},b.updater.process=function(a){var c;if(b.updater.queue[a.message])for(c in b.updater.queue[a.message])b.updater.queue[a.message][c](a);if(b.updater.queue["*"])for(c in b.updater.queue["*"])b.updater.queue["*"][c](a)},console.log("===> Connect:init");var c="http://gpsapi04.navi.cc:8888/socket",d=function(e){e>60&&(e=60),console.log("connecting to "+c+"...");var f=a.ws=new SockJS(c);f.onopen=function(){console.log("WebSocket connected")},f.onmessage=function(a){console.log("onmessage:",a.data);var c=JSON.parse(a.data);b.updater.process(c)},f.onclose=function(a){console.log("WebSocket disconnected"),setTimeout(function(){d(e*2)},e*1e3)}};return d(1),b.message="",b.send=function(b){this.message=b,a.$broadcast("channel_data","aaa")},b}]),"use strict",wwwGPSApp.controller("appCtrl",["$scope","$location",function(a,b){a.location=b,a.last_pos={lan:48,lon:35},a.list=["Встать","Сделать","Лечь спать"];for(var c=0;c<1;c++)a.list.push("Ollala");a.doAdd=function(){a.list.push("править баги")},console.log("appCtrl",a)}]),wwwGPSApp.controller("appCtrl2",["$scope",function(a){a.list=["Другой","список","дел"]}]),"use strict",wwwGPSApp.directive("mylist",function(){return{restrict:"E",transclude:!1,template:'<div>List:<ul><li ng-repeat="l in list"><mylistitem></mylistitem></li></ul></div>',link:function(a,b,c){console.log("mylist directive: link",a,b)}}}),wwwGPSApp.directive("mylistitem",function(){return{restrict:"E",transclude:!0,template:"<div>{{l}}</div>",link:function(a,b,c){console.log("mylistitem directive: link",a,b)}}}),wwwGPSApp.directive("mylist2",function(){return{restrict:"E",scope:{},transclude:!1,template:"<div>List2:<ul></ul></div>",link:function(a,b,c){var d=b[0].querySelector("ul");a.list=a.$parent.list,console.log("mylist2 directive: link",a,b,c,d),a.$watch("list",function(b,c){d.innerHTML="";for(var e=0;e<a.list.length;e++){var f=a.list[e],g=document.createElement("LI");g.innerHTML=f,d.appendChild(g)}},!0)}}}),wwwGPSApp.directive("gmap",["Connect",function(a){console.log("gmap:directive");var b=function(b,c,d){console.log("map directive: link",b,c,a);var e=new google.maps.LatLng(48.397,34.644),f={zoom:10,center:e,mapTypeId:google.maps.MapTypeId.ROADMAP},g=new google.maps.Map(c[0],f),h=new google.maps.Marker({map:g,position:e,title:"Rabbit",icon:{path:google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,fillColor:"yellow",fillOpacity:.8,strokeColor:"green",strokeWeight:4,scale:5},animation:null});a.updater.on("last_update",function(a){console.log("MAP last_update = ",a);var b=new google.maps.LatLng(a.point.lat,a.point.lon);h.setPosition(b)})};return{restrict:"A",transclude:!1,link:b}}]);
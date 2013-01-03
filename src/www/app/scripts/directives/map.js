wwwGPSApp.directive('gmap', ["Connect", function(C_onnect) {
    console.log('gmap:directive');
    var link = function(s_cope, e_lement, a_ttrs) {
        console.log('map directive: link', s_cope, e_lement, C_onnect);
        //element.innerHTML="<div>map</div>";
        var latlng = new google.maps.LatLng(48.397, 34.644);
        var myOptions = {
          zoom: 10,
          center: latlng,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(e_lement[0],
            myOptions);

        var lastpos = new google.maps.Marker({
          map: map,
          position: latlng,
          title: 'Rabbit',
          //icon: goldStar,
          icon: {
            path: google.maps.SymbolPath.BACKWARD_CLOSED_ARROW,
            fillColor: "yellow",
            fillOpacity: 0.8,
            strokeColor: "green",
            strokeWeight: 4,
            scale: 5
          },
          animation: null // google.maps.Animation.BOUNCE
        });
        //config.updater.add('last_update', function(msg) {
        var updater = C_onnect.updater.on('last_update', function(msg) {
            //if(msg.data.skey == skey) table.insertBefore(log_line(msg.data), table.firstChild);
            console.log('MAP last_update = ', msg);
            var newpos = new google.maps.LatLng(msg.point.lat, msg.point.lon);
            lastpos.setPosition(newpos);
        });

        /*console.log('config = ', config);
        scope.$on('channel_data', function(event, more){
            //var message = Connect.message;
            console.log(['Map on change_last', more]);
        });*/
        // listen on DOM destroy (removal) event, and cancel the next UI update
        // to prevent updating time ofter the DOM element was removed.
        e_lement.bind('$destroy', function() {
            console.log('MAP:destroy element')
            C_onnect.updater.remove(updater);
            //$timeout.cancel(timeoutId);
        });

    };
    return {
        restrict: 'A',
        transclude: false,
        //scope: {last_pos: '='},
        //template: '<div>List:<ul><li ng-repeat="l in list">{{l}}<i class="icon-arrow-right"></i><span>{{l}}</span></li></ul></div>',
        //template: '<div>MAP</div>',
        link: link/*,
        controller: ["$scope", "Connect", function($scope, Connect){
            console.log("map directive:controller", $scope, Connect);
        }]*/
    };
}]);

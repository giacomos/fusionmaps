/* global jQuery, google */
'use strict';

var map;
var markers = [];
function initMap() {
  var initialCenter = {lat: 0, lng: 0};
  map = new google.maps.Map(document.getElementById('map'), {
    center: initialCenter,
    zoom: 3
  });

  window.geocoder = new google.maps.Geocoder();
}

function handler(response){
}

function addMarker(location, title) {

  var marker = new google.maps.Marker({
    position: location,
    map: map,
    title: title
  });
  markers.push(marker);
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setMapOnAll(null);
}
// Shows any markers currently in the array.
function showMarkers() {
  setMapOnAll(map);
}
// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}

function auth() {
  var config = {
    'client_id': '68093915267.apps.googleusercontent.com',
    'scope': 'https://www.googleapis.com/auth/fusiontables',
    'immediate': false
  };
  debugger;
  gapi.auth.authorize(config, function () {
    console.log('login complete');
    console.log(gapi.auth.getToken());
  });
}

(function($){
  function codeAddress(address) {

      //In this case it gets the address from an element on the page, but obviously you  could just pass it to the method instead
    window.geocoder.geocode( { 'address' : address }, function( results, status ) {
      if( status === google.maps.GeocoderStatus.OK ) {
        if ( results.length < 1 ) {
          console.log('NO RESULT FOUND');
          return;
        }
        var location_type = results[0].geometry.location_type;
        if ( location_type !== 'ROOFTOP' && location_type !== 'GEOMETRIC_CENTER'){
          alert('Not a valid address');
          return;
        }

        var location = results[0].geometry.location;
        var address = results[0].formatted_address;
        $.ajax({
          dataType: 'json',
          url: 'addresses/create',
          data: {
            'lat': location.lat(),
            'lng': location.lng(),
            'address': address
          },
          success: function (data) {
            //In this case it creates a marker, but you can get the lat and lng from the location.LatLng
            if (data.result === 'ok'){
              map.setCenter( location );
              addMarker( location, address);
              $('.visited-addresses').append('<li><span>'+ address + '</span></li>');
            } else {
              alert(data.result);
            }

          }
        });
      } else {
        alert( 'Geocode was not successful for the following reason: ' + status );
      }
    } );
  }


  $(document).ready(function(){
    // auth();
    // $.ajax({
    //   url: 'https://www.googleapis.com/fusiontables/v2/tables?callback=handler&key=' + GOOGLE_API_KEY,
    //   data: {},
    //   success: function(data){
    //     debugger;
    //   }
    // });
    $('.addresses').on('click', 'a', function(ev){
      ev.preventDefault();
      var link = $(this);
      codeAddress(link.text());
    });
    $('.clear-addresses').on('click', function(ev){
      ev.preventDefault();
      deleteMarkers();
      $.ajax({
        dataType: 'json',
        url: 'addresses/remove_all',
        success: function (){
          $('.visited-addresses').empty();
        }
      });
    });
  });
})(jQuery);

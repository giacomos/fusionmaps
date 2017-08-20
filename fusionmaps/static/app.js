/* global jQuery, google, initial_markers */
'use strict';

var map;
var markers = [];

/*
* Callback function that initialize the google maps with our initial markers
*/
function initMap() {
  var initialCenter = {lat: 44.4833333, lng: 11.3333333};
  map = new google.maps.Map(document.getElementById('map'), {
    center: initialCenter,
    zoom: 3
  });

  window.geocoder = new google.maps.Geocoder();
  initial_markers.forEach(function(marker){
    addMarker(marker.location, marker.title);
  });
  showMarkers();
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

(function($){
  function codeAddress(address) {
    $('.spinner').spin();
    window.geocoder.geocode( { 'address' : address }, function( results, status ) {
      if( status === google.maps.GeocoderStatus.OK ) {
        if ( results.length < 1 ) {
          $('.spinner').spin(false);
          return;
        }
        var location_type = results[0].geometry.location_type;
        if ( location_type !== 'ROOFTOP' && location_type !== 'GEOMETRIC_CENTER'){
          alert('Not a valid address');
          $('.spinner').spin(false);
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
            if (data.result === 'ok'){
              map.setCenter( location );
              addMarker( location, address);
              $('.visited-addresses').append('<li><span>'+ address + '</span></li>');
              $('.spinner').spin(false);
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
    $('.addresses').on('click', 'a', function(ev){
      ev.preventDefault();
      var link = $(this);
      codeAddress(link.text());
    });
    $('.clear-addresses').on('click', function(ev){
      ev.preventDefault();
      $('.spinner').spin();
      deleteMarkers();
      $.ajax({
        dataType: 'json',
        url: 'addresses/remove_all',
        success: function (){
          $('.visited-addresses').empty();
          $('.spinner').spin(false);
        }
      });
    });
  });
})(jQuery);

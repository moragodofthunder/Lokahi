'use strict';

function initMap() {
    const plannerMap = new google.maps.Map(document.querySelector('#map'), {
      center: {
        lat: 37.601773,
        lng: -122.20287,
      },
      zoom: 11,
    });

  // Get coordinates from place user entered when creating new trip:
    const userAddress = document.querySelector('#trip-place').innerText;

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userAddress }, (results, status) => {
      if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;

        // // Create a marker
        new google.maps.Marker({
          position: userLocation,
          map,
        });

        // Zoom in on the geolocated location
        map.setCenter(userLocation);
        map.setZoom(12);
      } else {
        alert(`Geocode was unsuccessful for the following reason: ${status}`);
      }
    });
  };
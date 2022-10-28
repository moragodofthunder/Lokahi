
'use strict';

function initMap() {
    const map = new google.maps.Map(document.querySelector('#map'), {
      center: {
        lat: 37.601773,
        lng: -122.20287,
      },
      zoom: 11,
    });
  // Ask user to enter a location. Geocode the location to get its coordinates
  // and drop a marker onto the map.

    const userAddress = document.querySelector('#trip-place').innerText;

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userAddress }, (results, status) => {
      if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;    

        // // Create a marker
        const centerMarker = new google.maps.Marker({
          position: userLocation,
          map,
          icon: {
            url: "/static/img/green_pin.png",
            scaledSize: new google.maps.Size(25, 43)
          }
        });

        // Zoom in on the geolocated location
        map.setCenter(userLocation);
        map.setZoom(12);
      } 
    });

    document.querySelector('#submit-search').addEventListener('click', () => {

      const userSearch = document.querySelector('#place-search').value;
      console.log("Searched");
      console.log(userSearch);

      if (userSearch) {
        const geocoder2 = new google.maps.Geocoder();
        geocoder2.geocode({ address: userSearch }, (results, status) => {
          if (status === 'OK') {
            console.log("Result", results);
            // Get the coordinates of the search user's location
            const userSearchLocation = results[0].geometry.location;
            console.log(userSearchLocation);
            
            const userMarker = new google.maps.Marker({
                position: userSearchLocation,
                map,
                icon: {
                  url: "/static/img/purple_pin.png",
                  scaledSize: new google.maps.Size(25, 43)
                }
            });  
            
            map.setCenter(userSearchLocation);
            map.setZoom(12);
          }
          else {
            alert(`Geocode was unsuccessful for the following reason: ${status}`);
          }
        });
      }
    });
}
  
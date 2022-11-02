
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

        // Zoom in on the geolocated location
        map.setCenter(userLocation);
        map.setZoom(12);
       
      document.querySelector('#submit-search').addEventListener('click', () => {
        const userSearch = document.querySelector('#place-search').value;
        console.log(userSearch)
        const tripId = document.querySelector('#trip-id').value;
        console.log(tripId)
       // #get place Id, add to query String, in Python (see notes) 
        const queryString = new URLSearchParams({userSearch:userSearch, userLocation:userLocation}).toString();
        const url = `/api/place-search?${queryString}`;
    
        fetch(url)
        .then(result => result.json())
        .then(data => {
            console.log(data)
    
        for(const result of data.results) {
            if (result.photo_url === undefined) {
                result.photo_url = "/static/img/green_pin.png";
            }

            const placeLatLng = {lat: result.lat, lng: result.lng}
            console.log(placeLatLng)

                document.querySelector("#place-data").innerHTML += `
                <h3>${result.name}</h3>
                <h4>${result.types}</h4>
                <h4>${result.vicinity}</h4>
                <h4>(Rating: ${result.rating} stars)</h4>
                <h5>(${result.lat}, ${result.lng})</h5>
                <img class="place-img" src="${result.photo_url}">      
                `
                const placeMarker = new google.maps.Marker({
                  position: placeLatLng,
                  map,
                  icon: {
                    url: "/static/img/green_pin.png",
                    scaledSize: new google.maps.Size(25, 43)
                  }
                });
    
                map.setCenter(placeLatLng);
                map.setZoom(18);

            };
        }); 
    })}
      // document.querySelector('#submit-search').addEventListener('submit', (evt) => {
      //   evt.preventDefault();
        
      //   const userSearch = document.querySelector('#place-search').value;
      //   console.log(userSearch)
      //   const tripPlace = document.querySelector('#trip-place').innerText;
     
      //   var payload = {
      //     query: userSearch,
      //     fields: ['name', 'geometry'],
      //   };

      //   var service = new google.maps.places.PlacesService(map);

      //   service.findPlaceFromQuery(payload, function (results, status) {
      //     console.log(results);
      //     if (status === google.maps.places.PlacesServiceStatus.OK) {
      //       for (var i = 0; i < results.length; i++) {
      //         createMarker(results[i]);
      //         const resultMarker = new google.maps.Marker({
      //           position: userSearch,
      //           map,
      //           icon: {
      //             url: "/static/img/green_pin.png",
      //           }
      //         });

      //       }
      //       map.setCenter(results[0].geometry.location);
      //     }
      //   })
      // })

    });
}
  

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
            console.log('THIS IS THE DATE TYPE OF DATAAAAAAAA')
            console.log(typeof data)
            console.log(data)
    
        for(const result of data.results) {
            if (result.photo_url === undefined) {
                result.photo_url = "/static/img/green_pin.png";
            }
                document.querySelector("#place-data").innerHTML += `
                <div class="card" style="width: 18rem;">
                <img class="card-img-top" src="${result.photo_url}" alt="Card image cap"width="300" 
                height="200">
                  <div class="card-body">
                    <h5 class="card-title">${result.name}</h5>
                    <input type="checkbox" id="${result.name}" name="rest-choice" value="${result.name}">
                    <label for="${result.name}">${result.name} (Rating: ${result.rating} stars)</label>
                  </div>
              </div>`  
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
  
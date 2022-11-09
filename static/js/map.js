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
        
        document.querySelector("#category").value = ""
        document.querySelector("#notes").value = ""
        document.querySelector("#in-itinerary").value = ""

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

            const placeData = document.querySelector("#place-data");

            while (placeData.firstChild) {
            placeData.removeChild(placeData.firstChild);
            }   

                document.querySelector("#place-data").innerHTML += `
                <style>
                #place-data {
                  border-left: 2px solid black;
                  border-right: 2px solid black;
                  border-top: 2px solid black;
                }
                #place-info-menu {
                  display: block;
                  border-bottom: 2px solid black;
                  border-left: 2px solid black;
                  border-right: 2px solid black;
                }
                #place-img {
                  width: 100%;
                  height: auto;
                  border-radius: 60% 40% 64% 36% / 56% 58% 42% 44%;
                } 
                </style>
                <h3 id="ps-name">${result.name}</h3>
                <h5 id="ps-address">${result.vicinity}</h5>
                <h5 id="google-cat">${result.types.replace("_", " ")}</h5>
                <h6 id="google-rating">Rating: ${result.rating} stars</h6>
                <h6 id="ps-latlng">(lat: ${result.lat}, lng: ${result.lng})</h6>
                <img id="place-img" src="${result.photo_url}"> 
                `
                
                const placeMarker = new google.maps.Marker({
                  position: placeLatLng,
                  map,
                  icon: {
                    url: "/static/img/rainbow-pin.png",
                    scaledSize: new google.maps.Size(71, 107)
                  }
                });
    
                map.setCenter(placeLatLng);
                map.setZoom(18);

            };
            
        }); 
    })}
  });
}

document.querySelector("#save-place-db").addEventListener('submit', (evt) => {
  evt.preventDefault();

  const psFormInputs = {
    psCategory: document.querySelector("#category").value,
    psNotes: document.querySelector("#notes").value,
    psItinerary: document.querySelector("#in-itinerary").value,
    psCity: document.querySelector("#trip-city").innerText,
    psCountry: document.querySelector("#trip-country").innerText,
    psTripId: document.querySelector('#trip-id').value,
  }

  console.log(psFormInputs)

  fetch('/save-place', {
    method: 'POST',
    body: JSON.stringify(psFormInputs),
    headers: {
      'Content-Type': 'application/json',
    },
  }).then((response) => {
    console.log(response)
  })
})  
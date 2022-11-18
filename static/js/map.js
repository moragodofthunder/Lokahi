'use strict';

let tripLat = document.querySelector('#trip-lat').value;
let tripLng = document.querySelector('#trip-lng').value;

tripLat = Number(tripLat)
tripLng = Number(tripLng)

function initMap() {
    const map = new google.maps.Map(document.querySelector('#map'), {
      center: {
        lat: tripLat,
        lng: tripLng,
      },
      zoom: 12,
    });

      const tripLocation = `(${tripLat}, ${tripLng})`

      const placeInfo = new google.maps.InfoWindow();

            fetch('/api/all_places')
              .then((response) => response.json())
              .then((places) => {
                  for (const place of places) {
                    const placeInfoContent = `
                      <style>
                      #place-cat {
                        width: 200px,
                        height: auto, 
                      }
                      </style>

                      <div class="place-image></div>

                      <div class="place-info-content">
              
                      <ul class="place-info">
                          <li><b>Place: </b>${place.name}</li>
                          <li><b>In Itinerary: </b>${place.inItin}</li>
                          <li><b>Date: </b>${place.itinDT}</li>
                          <li><b>Location: </b>${place.placeLat}, ${place.placeLng}</li>
                          <li><b>Category: </b>${place.category}</li>
                          <img class="place-cat" src=${place.catEmoji} width="100">
                          
                      </ul>
                      </div>
                      `;
                    
                    const placeMarker = new google.maps.Marker({
                      position: {
                        lat: place.placeLat,
                        lng: place.placeLng,
                      },
                      title: `Name: ${place.name}`,
                      icon: {
                        url: `${place.catPin}`,
                        scaledSize: new google.maps.Size(71, 107)
                      },
                      map: map,
                    });
                    placeMarker.addListener('click', () => {
                      placeInfo.close();
                      placeInfo.setContent(placeInfoContent);
                      placeInfo.open(map, placeMarker);
                  });
                  }

      document.querySelector('#submit-search').addEventListener('click', () => {
        const userSearch = document.querySelector('#place-search').value;
        console.log(userSearch)
        const tripId = document.querySelector('#trip-id').value;
        console.log(tripId)
       // #get place Id, add to query String, in Python (see notes) 
        const queryString = new URLSearchParams({userSearch:userSearch, tripLocation:tripLocation}).toString();
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
                result.photo_url = "/static/img/cards/suitcase.png";
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
                  border-radius: 60% 40% 64% 36% / 56% 58% 42% 44%;
                  width: 100%;
                } 
                </style>
                <h3 id="ps-name">${result.name}</h3>
                <h5 id="ps-address">${result.vicinity}</h5>
                <h5 id="google-cat">${result.types.replace("_", " ")}</h5>
                <h6 id="google-rating">Rating: ${result.rating} stars</h6>
                <h6 id="ps-latlng">(lat: ${result.lat}, lng: ${result.lng})</h6>
                <img id="place-img" src="${result.photo_url}" value="${result.photo_url}"> 
                `
                
                const searchMarker = new google.maps.Marker({
                  position: placeLatLng,
                  map,
                  icon: {
                    url: "/static/img/pins/rainbow-pin.png",
                    scaledSize: new google.maps.Size(71, 107)
                  }
                });
    
                map.setCenter(placeLatLng);
                map.setZoom(18);

            };
            
            
            
        }); 
    })});
  


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
}) } 
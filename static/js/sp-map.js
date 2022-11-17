'use strict';

let place_pins = {
    
}

let tripLat = document.querySelector('#trip-lat').value;
let tripLng = document.querySelector('#trip-lng').value;

tripLat = Number(tripLat)
tripLng = Number(tripLng)

function initMap() {

    const spMap = new google.maps.Map(document.querySelector('#sp-map'), {
        center: {
            lat: tripLat,
            lng: tripLng
        },

        zoom: 12,
        });
    
    const placeInfo = new google.maps.InfoWindow();

    fetch('/api/all_places')
        .then((response) => response.json())
        .then((places) => {
            for (const place of places) {
                const placeInfoContent = `
                <div class="place-info-content">
                
                <ul class="place-info">
                    <li><b>Place: </b>${place.name}</li>
                    <li><b>In Itinerary: </b>${place.inItin}</li>
                    <li><b>Date: </b>${place.itinDT}</li>
                    <li><b>Category: </b>${place.category}</li>
                    <li><b>Location: </b>${place.placeLat}, ${place.placeLng}</li>
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
                    url: '/static/img/pins/1-breakfast-pin.png',
                    scaledSize: new google.maps.Size(71, 107)
                },
                map: spMap,
                });

            placeMarker.addListener('click', () => {
                placeInfo.close();
                placeInfo.setContent(placeInfoContent);
                placeInfo.open(spMap, placeMarker);
            });

        }
    })
        
}
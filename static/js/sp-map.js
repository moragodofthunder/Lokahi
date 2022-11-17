'use strict';

let place_pins = {
    Breakfast: '/static/img/pins/1-breakfast-pin.png',
    Lunch: '/static/img/pins/2-lunch-pin.png',
    Dinner: '/static/img/pins/3-dinner-pin.png',
    Streetfood: '/static/img/pins/4-streetfood-pin.png',
    Dessert: '/static/img/pins/5-dessert-pin.png',
    Cafe: '/static/img/pins/6-cafe-pin.png',
    Nightlife: '/static/img/pins/7-nightlife-pin.png',
    Bar/Pub: '/static/img/pins/8-bar-pin.png',
    Shopping: '/static/img/pins/9-shopping-pin.png',
    Groceries: '/static/img/pins/10-grocery-pin.png',
    Convenience Store: '/static/img/pins/11-kombini-pin.png',
    Outdoor Market: '/static/img/pins/12-farmers-market-pin.png',
    Covered Market: '/static/img/pins/13-bazaar-pin.png',
    Bookstore/Library: '/static/img/pins/14-bookstore-pin.png',
    Train Station: ;
    Museum: ;
    Landmark: ;
    Photo Spot: ;
    Temple/Shrine/Worship: ;
    Entertainment: ;
    Music: ;
    Hot Spring: ;
    Beach: ;
    Park: ;
    Hiking: ;
    Surfing: ;
    Workspace: ;
    COVID Testing: ;
    Miscellaneous: ;

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
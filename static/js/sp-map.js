'use strict';

let place_pins = {
    'Breakfast': '/static/img/pins/1-breakfast-pin.png',
    'Lunch': '/static/img/pins/2-lunch-pin.png',
    'Dinner': '/static/img/pins/3-dinner-pin.png',
    'Streetfood': '/static/img/pins/4-streetfood-pin.png',
    'Dessert': '/static/img/pins/5-dessert-pin.png',
    'Cafe': '/static/img/pins/6-cafe-pin.png',
    'Nightlife': '/static/img/pins/7-nightlife-pin.png',
    'Bar/Pub': '/static/img/pins/8-bar-pin.png',
    'Shopping': '/static/img/pins/9-shopping-pin.png',
    'Groceries': '/static/img/pins/10-grocery-pin.png',
    'Convenience Store': '/static/img/pins/11-kombini-pin.png',
    'Outdoor Market': '/static/img/pins/12-farmers-market-pin.png',
    'Covered Market': '/static/img/pins/13-bazaar-pin.png',
    'Bookstore/Library': '/static/img/pins/14-bookstore-pin.png',
    'Train Station': '/static/img/pins/15-train-pin.png',
    'Museum': '/static/img/pins/16-museum-pin.png',
    'Landmark': '/static/img/pins/17-landmark-pin.png',
    'Photo Spot': '/static/img/pins/18-photo-pin.png',
    'Temple/Shrine/Worship': '/static/img/pins/19-shrine-pin.png',
    'Entertainment': '/static/img/pins/20-entertain-pin.png',
    'Music': '/static/img/pins/21-music-pin.png',
    'Hot Spring': '/static/img/pins/22-onsen-pin.png',
    'Beach': '/static/img/pins/23-beach-pin.png',
    'Park': '/static/img/pins/24-park-pin.png',
    'Hiking': '/static/img/pins/25-hiking-pin.png',
    'Surfing': '/static/img/pins/26-surf-pin.png',
    'Workspace': '/static/img/pins/27-work-pin.png',
    'COVID Testing': '/static/img/pins/28-covid-pin.png',
    'Miscellaneous': '/static/img/pins/29-misc-pin.png',

}

let cat_emojis = {
    'Breakfast': '/static/img/emojis/1-breakfast-emoji.png',
    'Lunch': '/static/img/emojis/2-lunch-emoji.png',
    'Dinner': '/static/img/emojis/3-dinner-emoji.png',
    'Streetfood': '/static/img/emojis/4-streetfood-emoji.png',
    'Dessert': '/static/img/emojis/5-dessert-emoji.png',
    'Cafe': '/static/img/emojis/6-cafe-emoji.png',
    'Nightlife': '/static/img/emojis/7-nightlife-emoji.png',
    'Bar/Pub': '/static/img/emojis/8-bar-emoji.png',
    'Shopping': '/static/img/emojis/9-shopping-emoji.png',
    'Groceries': '/static/img/emojis/10-grocery-emoji.png',
    'Convenience Store': '/static/img/emojis/11-kombini-emoji.png',
    'Outdoor Market': '/static/img/emojis/12-farmers-market-emoji.png',
    'Covered Market': '/static/img/emojis/13-bazaar-emoji.png',
    'Bookstore/Library': '/static/img/emojis/14-bookstore-emoji.png',
    'Train Station': '/static/img/emojis/15-train-emoji.png',
    'Museum': '/static/img/emojis/16-museum-emoji.png',
    'Landmark': '/static/img/emojis/17-landmark-emoji.png',
    'Photo Spot': '/static/img/emojis/18-photo-emoji.png',
    'Temple/Shrine/Worship': '/static/img/emojis/19-shrine-emoji.png',
    'Entertainment': '/static/img/pins/20-entertain-pin.png',
    'Music': '/static/img/pins/21-music-pin.png',
    'Hot Spring': '/static/img/pins/22-onsen-pin.png',
    'Beach': '/static/img/pins/23-beach-pin.png',
    'Park': '/static/img/pins/24-park-pin.png',
    'Hiking': '/static/img/pins/25-hiking-pin.png',
    'Surfing': '/static/img/pins/26-surf-pin.png',
    'Workspace': '/static/img/pins/27-work-pin.png',
    'COVID Testing': '/static/img/pins/28-covid-pin.png',
    'Miscellaneous': '/static/img/pins/29-misc-pin.png',
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
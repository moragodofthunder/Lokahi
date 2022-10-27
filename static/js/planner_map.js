'use strict';

function initMap() {
    const tokyoCoords = {
      lat: 35.6762,
      lng: 139.6503,
    };
  
    const tokyoMap = new google.maps.Map(document.querySelector('#map'), {
      center: tokyoCoords,
      zoom: 11,
    });

    const donQMarker = new google.maps.Marker({
        position: {lat: 35.69398146755949, lng: 139.70178595767092},
        title: 'Don Quijote Kabukicho',
        map: tokyoMap,
        icon: {
            url: '/static/img/green_pin.png',
          scaledSize: {
            width: 25,
            height: 45,
          },
        },
    });


    const donQInfo = new google.maps.InfoWindow({
        content: '<h3>Don don don Quijote</h3>',
    });

    donQInfo.open(tokyoMap, donQMarker)

    const markerInfo = `
      <h1>${marker.title}</h1>
      <div class="category-menu">
        <form>
            <label for="category">Choose place category</label>
            <select id="category" name="category">
                <option value="breaky">Breakfast spot</option>
                <option value="lunch">Lunch place</option>
                <option value="dinner">Dinner spot</option>
                <option value="streetfood">Street food/snack</option>
                <option value="dessert">Dessert place</option>
                <option value="night">Nightlife</option>
                <option value="bar">Bar or pub</option>
                <option value="train">Train station</option>
                <option value="shop">Shopping</option>
                <option value="books">Bookstore or library</option>
                <option value="museum">Museum</option>
                <option value="history">Historical landmark</option>
                <option value="photo">Photo spot</option>
                <option value="temple">Temple/shrine/worship</option>
                <option value="entertain">Entertainment</option>
                <option value="music">Music venue</option>
                <option value="bath">Sento/onsen/hotspring</option>
                <option value="beach">Beach</option>
                <option value="park">Park</option>
                <option value="workspace">Workspace</option>
                <option value="covid">COVID Testing center</option>
            </select>
            <input type="submit" value="Add to Saved Places">        
        </form>
    </div>
    <div class="itinerary-menu">
        <form>
            <label for="in_itinerary">Add to itinerary</label>
            <select id="in_itinerary" name="in_itinerary">
                <option value="day-1">Day 1</option>
                <option value="day-2">Day 2</option>
                <option value="day-3">Day 3</option>
                <option value="day-4">Day 4</option>
                <option value="day-5">Day 5</option>
                <option value="day-6">Day 6</option>
                <option value="day-7">Day 7</option>
            </select>
            <input type="submit" value="Add to Itinerary">        
        </form>
    </div>
    <div class="notes">
        <form>
            <label for="notes">Notes:</label>
            <input type="text" id="notes" name="notes">
            <input type="submit" value="Add Special Note">
        </form>
    </div>
    `;

    const infoWindow = new google.maps.InfoWindow({
        content: markerInfo,
        maxWidth: 200,
      });
  
      marker.addListener('click', () => {
        infoWindow.open(basicMap, marker);
      });
    }

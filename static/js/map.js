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

            const placeData = document.querySelector("#place-data");

            while (placeData.firstChild) {
            placeData.removeChild(placeData.firstChild);
            }
                document.querySelector("#place-data").innerHTML += `
                <style>
                #place-data {
                  border-style: solid;
                  border-width: 2px;
                  border-color: black;
                } 
                </style>
                <h3>${result.name}</h3>
                <h4>${result.types.replace("_", " ")}</h4>
                <h4>${result.vicinity}</h4>
                <h4>(Rating: ${result.rating} stars)</h4>
                <h5>(${result.lat}, ${result.lng})</h5>
                <img class="place-img" src="${result.photo_url}"> 
                
                <div class="category-menu">
                  <form>
                      <select id="category" name="category">
                          <option value="">Choose a place category</option>
                          <option value="breaky">Breakfast spot</option>
                          <option value="lunch">Lunch place</option>
                          <option value="dinner">Dinner spot</option>
                          <option value="streetfood">Street Food or Snack</option>
                          <option value="dessert">Dessert place</option>
                          <option value="cafe">Cafe</option>
                          <option value="night">Nightlife</option>
                          <option value="bar">Bar or pub</option>
                          <option value="train">Train station</option>
                          <option value="shop">Shopping</option>
                          <option value="books">Bookstore or Library</option>
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
                          <option value="misc">Miscellaneous</option>
                      </select>       
                  </form>
              </div>

              <div class="itinerary-menu">
                <form>
                    <select id="in_itinerary" name="in_itinerary">
                        <option value="">Add to itinerary (optional)</option>
                        {% for date in travel_dates %}
                        <option value="{{ date }}">{{ date }}</option>
                        {% endfor %}
                    </select>        
                </form>
              </div>

              <div class="notes">
                <form>
                    <label for="notes">Notes:</label>
                    <input type="text" id="notes" name="notes">
                </form>
                <input type="submit" value="Save Place"> 
              </div>
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
  });
}
  
'use strict';

function initMap() {
    const plannerMap = new google.maps.Map(document.querySelector('#map'), {
      center: {
        lat: 37.601773,
        lng: -122.20287,
      },
      zoom: 11,
    });
  // Get coordinates from place user entered when creating new trip:
  
    const userAddress = document.querySelector('#trip-place').innerText;

    // const userCountry = document.querySelector('#trip-country').innerText;

    // const userSearchPlace = document.querySelector("place-search").innerText;

    // if (userCountry in countryCodes)
    //     {const userCountryCode = countryCodes[userCountry]};

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userAddress }, (results, status) => {
      if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;

        // // Create a marker
        // new google.maps.Marker({
        //   position: userLocation,
        //   map,
        // });

        // Zoom in on the geolocated location
        map.setCenter(userLocation);
        map.setZoom(12);
      } else {
        alert(`Geocode was unsuccessful for the following reason: ${status}`);
      }
    });

//     const markerInfo = `
//     <h1>${marker.title}</h1>
//     <div class="category-menu">
//       <form>
//           <label for="category">Choose place category</label>
//           <select id="category" name="category">
//               <option value="breaky">Breakfast spot</option>
//               <option value="lunch">Lunch place</option>
//               <option value="dinner">Dinner spot</option>
//               <option value="streetfood">Street food/snack</option>
//               <option value="dessert">Dessert place</option>
//               <option value="night">Nightlife</option>
//               <option value="bar">Bar or pub</option>
//               <option value="train">Train station</option>
//               <option value="shop">Shopping</option>
//               <option value="books">Bookstore or library</option>
//               <option value="museum">Museum</option>
//               <option value="history">Historical landmark</option>
//               <option value="photo">Photo spot</option>
//               <option value="temple">Temple/shrine/worship</option>
//               <option value="entertain">Entertainment</option>
//               <option value="music">Music venue</option>
//               <option value="bath">Sento/onsen/hotspring</option>
//               <option value="beach">Beach</option>
//               <option value="park">Park</option>
//               <option value="workspace">Workspace</option>
//               <option value="covid">COVID Testing center</option>
//           </select>
//           <input type="submit" value="Add to Saved Places">        
//       </form>
//   </div>
//   <div class="itinerary-menu">
//       <form>
//           <label for="in_itinerary">Add to itinerary</label>
//           <select id="in_itinerary" name="in_itinerary">
//               <option value="day-1">Day 1</option>
//               <option value="day-2">Day 2</option>
//               <option value="day-3">Day 3</option>
//               <option value="day-4">Day 4</option>
//               <option value="day-5">Day 5</option>
//               <option value="day-6">Day 6</option>
//               <option value="day-7">Day 7</option>
//           </select>
//           <input type="submit" value="Add to Itinerary">        
//       </form>
//   </div>
//   <div class="notes">
//       <form>
//           <label for="notes">Notes:</label>
//           <input type="text" id="notes" name="notes">
//           <input type="submit" value="Add Special Note">
//       </form>
//   </div>
//   `;
    autocomplete = new google.maps.places.Autocomplete(
        document.querySelector("place-search").innerText
    ), {
        componentRestrictions: {'country': [userCountryCode]},
        fields: ['geometry', 'name'],
        types: ['establishment']
    }

    autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();
        new google.maps.Marker({
            position: userLocation.geometry.location,
            title: userLocation.name,
            content: markerInfo,
            map: plannerMap,

        })

    userSearchPlace.addListener("submit", () => {
        userSearchPlace.getPlace();
        new google.maps.Marker({
            position: userLocation.geometry.location,
            title: userLocation.name,
            content: markerInfo,
            map: plannerMap,
        })
    });

    
  };

  //__________________________________________________________________________________
  //VERSION 2:

  'use strict';

function initMap() {
    const plannerMap = new google.maps.Map(document.querySelector('#map'), {
      center: {
        lat: 37.601773,
        lng: -122.20287,
      },
      zoom: 11,
    });

  // Get coordinates from place user entered when creating new trip:
    const userAddress = document.querySelector('#trip-place').innerText;

    // const userCountry = document.querySelector('#trip-country').innerText;

    // const userSearchPlace = document.querySelector("place-search").innerText;

    // if (userCountry in countryCodes)
    //     {const userCountryCode = countryCodes[userCountry]};
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ address: userAddress }, (results, status) => {
      if (status === 'OK') {
        // Get the coordinates of the user's location
        const userLocation = results[0].geometry.location;

        //Stuff inside info box:
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
      const infowindow = new google.maps.InfoWindow({
        content: markerInfo,
        ariaLabel: `${marker.title}`,
      });

        // // Create a marker
        const marker = new google.maps.Marker({
          position: userLocation,
          map,
        });

        marker.addListener("click", () => {
            infowindow.open({
                anchor: marker,
                map,
            });
        });

        // Zoom in on the geolocated location
        map.setCenter(userLocation);
        map.setZoom(12);
      } else {
        alert(`Geocode was unsuccessful for the following reason: ${status}`);
      }
    });
  };


  '</div>' +
  '<div class="itinerary-menu">' +
      '<form>' +
          '<label for="in_itinerary">Add to itinerary</label>' +
          '<select id="in_itinerary" name="in_itinerary">' +
              '<option value="day-1">Day 1</option>' +
              '<option value="day-2">Day 2</option>' +
              '<option value="day-3">Day 3</option>' +
              '<option value="day-4">Day 4</option>' +
              '<option value="day-5">Day 5</option>' +
              '<option value="day-6">Day 6</option>' +
              '<option value="day-7">Day 7</option>' +
          '</select>' +
          '<input type="submit" value="Add to Itinerary">' +        
      '</form>' +
  '</div>' +
  '<div class="notes">' +
      '<form>' +
          '<label for="notes">Notes:</label>' +
          '<input type="text" id="notes" name="notes">' +
          '<input type="submit" value="Add Special Note">' +
      '</form>' +
  '</div>' +




    //Content for inside infoWindow:
    const markerInfo = 
    '<div class="category-menu">' +
          '<label for="category">Choose place category</label>' +
          '<select id="category" name="category">' +
              '<option value="breaky">Breakfast spot</option>' +
              '<option value="lunch">Lunch place</option>' +
              '<option value="dinner">Dinner spot</option>' +
              '<option value="streetfood">Street food/snack</option>' +
              '<option value="dessert">Dessert place</option>' +
              '<option value="night">Nightlife</option>' +
              '<option value="bar">Bar or pub</option>' +
              '<option value="train">Train station</option>' +
              '<option value="shop">Shopping</option>' +
              '<option value="books">Bookstore or library</option>' +
              '<option value="museum">Museum</option>' +
              '<option value="history">Historical landmark</option>' +
              '<option value="photo">Photo spot</option>' +
              '<option value="temple">Temple/shrine/worship</option>' +
              '<option value="entertain">Entertainment</option>' +
              '<option value="music">Music venue</option>' +
              '<option value="bath">Sento/onsen/hotspring</option>' +
              '<option value="beach">Beach</option>' +
              '<option value="park">Park</option>' +
              '<option value="workspace">Workspace</option>' +
              '<option value="covid">COVID Testing center</option>' +
          '</select>' +
          '<button type="button" id="add-place">Add to Saved Places</button>' +        
      '</form>' +
  '</div>' +
  '<div class="itinerary-menu">' +
      '<form>' +
          '<label for="in_itinerary">Add to itinerary</label>' +
          '<select id="in_itinerary" name="in_itinerary">' +
              '<option value="day-1">Day 1</option>' +
              '<option value="day-2">Day 2</option>' +
              '<option value="day-3">Day 3</option>' +
              '<option value="day-4">Day 4</option>' +
              '<option value="day-5">Day 5</option>' +
              '<option value="day-6">Day 6</option>' +
              '<option value="day-7">Day 7</option>' +
          '</select>' +
          '<input type="submit" value="Add to Itinerary">' +        
      '</form>' +
  '</div>' +
  '<div class="notes">' +
      '<form>' +
          '<label for="notes">Notes:</label>' +
          '<input type="text" id="notes" name="notes">' +
          '<input type="submit" value="Add Special Note">' +
      '</form>' +
  '</div>' +
  `<script>
    document.querySelector("#add-place").addEventListener("click", (evt) => {
      evt.preventDefault()
      console.log("It worked!")
    });
  </script>
  `;

  const infowindow = new google.maps.InfoWindow({
    content: markerInfo,
    ariaLabel: userLocation.title
});


//Submit event listener I don't want to lose:
document.querySelector('#search-bar').addEventListener('submit', (evt) =>
        evt.preventDefault());

// Geocoder that puts purple marker on map of location user searches for:
//Put inside of "initMap" but after green pin is placed.

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
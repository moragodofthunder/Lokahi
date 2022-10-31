'use strict';

// let request = {
//     fields: ['name', 'geometry']
// };

// let service = new google.maps.places.PlacesService(map);
// service.getDetails(request, callback);



document.querySelector('#submit-search').addEventListener('click', () => {
    const userSearch = document.querySelector('#place-search').value;
    console.log(userSearch)
    const tripId = document.querySelector('#trip-id').value;
    console.log(tripId)
   // #get place Id, add to query String, in Python (see notes) 
    const queryString = new URLSearchParams({userSearch:userSearch, tripId:tripId}).toString();
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
})
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
            <h3>${result.name}</h3>
            <img class="place-img" src="${result.photo_url}">      
            <h4>(Rating: ${result.rating} stars)</h4>
            `  
        };
    }); 
})
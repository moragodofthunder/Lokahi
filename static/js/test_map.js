'use strict';

function initMap() {
    const testMap = new google.maps.Map(document.querySelector('#test-map'), {
        center: {
            lat: 35.72691,
            lng: 139.773659,
        },

        zoom: 18,
        mapId: '6a773bffa03dfac9',

    });

    const placeMarker = new google.maps.Marker({
        position: {
            lat: 35.72691,
            lng: 139.773659,
        },
        title: `Habutae Dango Shop Marked by Mora`,
        icon: {
            url: "/static/img/emojis/4-streetfood-emoji.png",
            scaledSize: new google.maps.Size(107, 107)
        },
        map: testMap,
    });
    
    const windowInfo = new google.maps.InfoWindow();

    const windowInfoContent = `
    <style>
    #mora-pic {
        width: 200px;
        border-radius: 50%;
      }
    .place-info {
        width: 350px;
    }
    </style>
    <div class="place-info">
    <p><strong>Habutae Dango</strong></p>
    <p>Habutae Dango is over 200 years old. It was founded in 1819 and is known for their an-dango (redbean covered mochi) 
    and yakidango (mochi with soy sauce flavor that is grilled over a charcoal grill). 
    </p>
    <p>Recommended by:</p>
    <p>Mora, <em>Lōkahi Founder</em></p>
    <img class="mora-pic" src="https://res.cloudinary.com/lokahi-cloud/image/upload/v1669947181/n7sdm294i6d7kke2lch0.jpg" width="100">
    </div>
    `;

    placeMarker.addListener('click', () => {
        windowInfo.close();
        windowInfo.setContent(windowInfoContent);
        windowInfo.open(testMap, placeMarker);
    });
}
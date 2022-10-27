'use strict';

let autocomplete = new google.maps.places.Autocomplete(
    document.querySelector("#trip-country"),
    {
        componentRestrictions: { country: ["us"] },
        fields: ["address_components"],
        types: ["address"]
    }
)
autocomplete.addListener("place_changed", fillInAddress);
function fillInAddress() {
    const place = autocomplete.getPlace();
    for (const component of place.address_components) {
        const componentType = component.types[0];

        switch (componentType) {
            case "locality":
                document.querySelector("#locality").value = 
                    component.long_name;
                
                break;
        }
    }
}



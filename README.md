<img src="/static/img/logos/lokahi-logo-rg.png" alt="Lokahi Logo" name="Lokahi Rainbow Logo" width="250">

by [Mora Napoleon](https://www.linkedin.com/in/moranapoleon/) | <a href="mailto:moragodofthunder@gmail.com?subject=Lokahi on GitHub">moragodofthunder@gmail.com</a> | [See the Demo](https://youtu.be/svxZKXab3UI) | [lokahi.travel](https://lokahi.travel)

<span>
<img src="/static/img/buttons/pins-and-ti.png" alt="Map Pins and Ti Leaves" width="200">
<img src="/static/img/favicons/Pink-suitcase-with-flowers.png" alt="Suitcase Full of Flowers" width="200">
<img src="/static/img/favicons/tp-icon.png" alt="Map with Magnifying Glass" width="200">
</span>

# Table of Contents
* [Tech Stack](#tech-stack)
* [About Lōkahi](#about-lokahi)
* [Features](#features)
* [About the Emojis](#emojis)
* [Looking Ahead](#future)
* [About the Developer](#about-mora)
* [Acknowledgements](#acknowledgements)
* [Install Lōkahi](#install-lokahi)
* [Licenses](#licenses)


# <a name="tech-stack"></a>Tech Stack
<ul>
<li> <strong>Frontend:</strong> HTML | JavaScript | CSS | Bootstrap</li>
<li> <strong>Backend:</strong> Python | Flask | Jinja | SQLAlchemy</li>
<li> <strong>APIs:</strong> Google Maps | Google Geocoding | Google Places | Cloudinary</li>
</ul>

# <a name="about-lokahi"></a>About Lōkahi
Lōkahi is a collaborative travel planning web app for friends who want to make planning travel together easier. Inspired by the Hawaiian word for "together", Lōkahi (pronounced "loh-KAH-hee") allows users to find places on a map, categorize them by type, and add them to their itinerary without ever having to make a separate spreadsheet. 

When a new trip is created, users are routed to a searchable map of their destination city. When a place is saved, the place pin and itinerary table item display with matching emojis and colors. If a user shares a trip with friends, all users can save places, add to the itinerary, or upload an image for the trip card. 

Lōkahi is map-based so users can see if their plans to visit certain places are actually feasible in one day.

# <a name="features"></a>Features
## Account Creation and Login
On sign up the user is prompted to enter their email address, password, first name, last name, and favorite color from a dropdown menu. They then log in with their email and password after a flash message confirms their successful account creation.

![GIF of Account Creation](/static/img/gifs/1-make-acct.gif)

## Profile Page
The user's default avatar is chosen based on the favorite color they chose at sign up, but they can choose to upload a personal profile image which uses Cloudinary's AI to crop the image to size and automatically zoom in to the most interesting part of the photo.

![GIF of Profile Image Upload](/static/img/gifs/2-prof-img.gif)

The user can also choose to add other Lōkahi users to their Travel 'Ohana (friends list) by email address, so they can include their friends and family in their trip planning.

![GIF of Adding to Travel 'Ohana](/static/img/gifs/3-add-to-ohana.gif)

## Trip Creation and Sharing

When a trip is created, users are automatically routed to a searchable map of their destination city, created with the Google Maps API. 

![GIF of New Trip Creation](/static/img/gifs/4-new-trip.gif)

If a trip is shared with them via another user, it will automatically show up under the trips they are in charge of planning. Past trips and shared past trips will populate dependant on whether the trip has ended based on the current date.

![GIF of Trip Card Organization](/static/img/gifs/5-list-of-trips.gif)

If the user wants to share the trip with any of the members of their Travel 'Ohana, friends can be added on the trip details page and their friends’ profile images will also show up on the edge of each trip card.

![GIF of Adding Friends to Trip](/static/img/gifs/6-add-friend-to-trip.gif)

All friends who are traveling together can save places into the itinerary, add to the list of saved places, and upload an image to represent the trip so they can get excited for upcoming trips or relive travel memories every time they log in.

![GIF of New Trip Image Upload](/static/img/gifs/7-new-trip-img.gif)

## Searching and Saving Places

With the help of the Google Places API, users can search for places by name and see information about each place like the address, the average rating from Google reviews, and a photo of the place. I used an AJAX call to display this information in a sidebar without reloading the page and used JavaScript DOM manipulation to display a menu that allows users to save a place, add any special notes, and add the place to their itinerary.

![GIF of Searching for a Place in Trip Planner](/static/img/gifs/8-place-search.gif)

If a user chooses to save a place for their trip, they can categorize the type of place using one of the 29 categories provided and the place will show up on the map of saved places, or the user can choose to categorize the place as ‘Miscellaneous’ if nothing fits the bill. 'COVID Testing Centers' and 'Workspaces' were included in the list of categories to help users navigate modern travel.

![GIF of Categorizing a Place](/static/img/gifs/9-categories.gif)

## Map of Saved Places

When a user clicks on a pin of a saved place, it queries the Postgresql database using SQLAlchemy to retrieve information about each place the user saved along with any special notes the user input and information about who saved which place.

![GIF of Clicking Through Map of Saved Places](/static/img/gifs/10-sp-map.gif)


## Itinerary Tables and Color/Emoji Coordination

The pin, itinerary table item, and the saved places table item for each saved place display on the saved places map and trip details pages with coordinating emojis and colors so the user can see the types of places they plan to travel to at a glance. The automatically created itinerary tables also eliminate the need to make a spreadsheet in a separate app.

![GIF of Color Coordination](/static/img/gifs/11-color-coord.gif)

# <a name="emojis"></a>About the Emojis

All emojis, map pins, and table banners were digitally drawn by me for the Lōkahi app. The standard Lōkahi emojis each represent a category and a piece of my Hawaiian and Japanese culture.

<span>
<img src="/static/img/readme-pins/pins-1.png" alt="rainbow-pins-1" width="270">
<img src="/static/img/readme-pins/pins-2.png" alt="rainbow-pins-2" width="270">
<img src="/static/img/readme-pins/pins-3.png" alt="rainbow-pins-3" width="270">
</span>
<br>
<span>
<img src="/static/img/emojis/12-farmers-market-emoji.png" alt="farmers-market-basket" width="270">
<img src="/static/img/emojis/22-onsen-emoji.png" alt="japanese-onsen" width="270">
<img src="/static/img/emojis/21-music-emoji.png" alt="hawaiian-man-singing-with-ukulele" width="270">
</span>

The default trip image of a suitcase has a sticker to represent each of my friends, my cohort-mates from Hackbright Academy, my Hackbright Academy teachers, and myself.

<img src="/static/img/cards/suitcase.png" alt="pink-suitcase-covered-in-stickers">

# <a name="future"></a>Looking Ahead

Lōkahi is the first full-stack web application I have built and I have lots of features that I am still building as it’s my goal to make it the most powerful collaborative travel planning tool it can be. A "calm mode" is coming for those who don't like the psychedelic style of the site. In the future users will also have the ability to set their own category colors and send their itineraries to people who aren't traveling with them in case they need to keep anyone in the loop about their whereabouts while they are away. There are also new emoji sets for other countries in the works.

# <a name="about-mora"></a>About the Developer

I am very passionate about my Hawaiian and Asian heritage and have worked on many projects that celebrate my culture, including a children's book about Hawaiian pa'u riders. I previously worked in customer service for over ten years everywhere from retail, to startups, to working in veterinary medicine.

But my passion for tech was sparked while working for a startup that let me work side by side with their small developer team to give feedback about user experience and see how changes could be implemented on both the front and back end.

I have always enjoyed learning systems and finding solutions to problems (sometimes in very unique and unexpected ways). In customer service, helping people was always my number one priority and as a software engineer I want to continue helping people and educating myself on new and exciting solutions. 

I am also artistic and passionate about learning animation and how to bridge the gap between art and technology. I am currently starting my Three.js Journey and teaching myself Blender so I can incorporate 3D designs into my web development.

Please [connect with me](https://www.linkedin.com/in/moranapoleon/) on LinkedIn!

<img src="/static/img/logos/Flower-portrait.png" alt="photo-of-mora" width="350">

# <a name="acknowledgements"></a>Acknowledgements

<strong>Advisors:</strong>
<ul>
<li>Steve Chait</li>
<li>Trew Boisvert</li>
</ul>

<strong>Mentor:</strong>
<ul>
<li>Lee Wang</li>
</ul>

<strong>Special Thanks:</strong>
<ul>
<li>Zoe Gotch-Strain</li>
<li>Jen Brissman</li>
<li>Joe Buckley</li>
<li>Nazan Aktas</li>
<li>Marshall Byrne</li>
</ul>

# <a name="install-lokahi"></a>Install Lōkahi

1. Clone this repository
```
git clone https://github.com/moragodofthunder/Lokahi.git
```
<em>Optional:</em> Create and activate a virtual environment
```
pip3 install virtualenv
virtualenv env
source env/bin/activate
```
2. Install dependencies
```
pip3 install -r requirements.txt
```
3. Create environmental variables to hold your API keys in a secrets.sh file. You'll need to create your own Google Maps, Google Places, Google Geocoding, and Cloudinary API keys:
```
export cloud_name="create your own cloudindary name/account"
export cloud_api_key="once you do this they will provide you a key which you will put here"
export cloud_api_secret="use your own secret of course, shhh"
export google_api_key="create your own google account account and enter your key into your own secrets.sh file
```
4. Create a database & seed sample data:
```
createdb my_lokahi
python3 seed_database.py
```
5. Run the app on localhost:
```
source secrets.sh
python3 lokahi_server.py
```

# <a name="licenses"></a>Licenses

All artwork on the Lōkahi GitHub repository and on lokahi.travel is copyrighted and may not be reproduced or used for commercial purposes by anyone but the artist. 










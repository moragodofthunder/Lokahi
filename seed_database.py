"""Script to seed database."""

import os
from random import choice, randint, sample
from datetime import datetime

import model
import lokahi_server
import crud
import requests

api_key = os.environ['YOUR_API_KEY']

os.system("dropdb lokahi")
os.system("createdb lokahi")

model.connect_to_db(lokahi_server.app)
model.db.create_all()

places = {"Budapest": "Hungary", "Tokyo": "Japan", "Mexico City": "Mexico",
"Gdansk": "Poland", "London": "England", "Honolulu": "United States", "Istanbul": "Turkey",
"Barcelona": "Spain", "Paris": "France", "Amsterdam": "Netherlands", "Glasgow": "Scotland"}

cities = []

cities = list(places.keys())

names = {"Joe": "Shmoe", "Marshy": "Parshy", "Nizzle": "Fo'Shizzle", "Veggie": "MoMo",
"HMS": "Zow"}

f_names = []

f_names = list(names.keys())

profile_pics = ["/static/img/avatars/purple-profile.png", "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668557833/n6bjegtzrb3c1fkhttzz.png",
 "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668558178/ndoe39a4bboawu0bo5du.png", "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668558217/vykblvhfizwomd6fqgzr.png",
 "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668558257/y1vbha6vo7njtzpduxta.png"]

#Create 5 fake users
for n in range(5):
    # i = randint(0, 6)
    email = f"user{n}@test.com"
    password = "1234"
    fname = choice(f_names)
    print(f"THIS IS THE FIRST NAAAAAME: {fname}")
    lname = names[fname]
    profile_img = choice(profile_pics)  

    user = crud.create_user(email, password, fname, lname, profile_img)
    model.db.session.add(user)
    model.db.session.commit()

#Give each user 6 fake trips:
    for i in range(6):
        get_city = sample(cities, 1)
        trip_city = "".join(get_city)
        trip_country = places[trip_city]

        address = f"{trip_city}, {trip_country}"
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()

        if api_response_dict['status'] == 'OK':
            trip_lat = api_response_dict['results'][0]['geometry']['location']['lat']
            trip_lng = api_response_dict['results'][0]['geometry']['location']['lng']

        random_start = randint(1, 20)
        start_date = f"2022-12-{random_start}"
        random_end = random_start + 5
        end_date = f"2022-12-{random_end}"
        trip_name = f"Trip #{i + 1}: {trip_city}, {trip_country}"
        trip_img = "/static/img/cards/suitcase.png"

        trip = crud.create_trip(trip_name, trip_country, 
        trip_city, start_date, end_date, trip_img, trip_lat, trip_lng, user.user_id)
        model.db.session.add(trip)

if user.user_id == 2:
    user.profile_img = "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668557833/n6bjegtzrb3c1fkhttzz.png"

elif user.user_id == 1:
    user.profile_img = "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668558178/ndoe39a4bboawu0bo5du.png"

elif user.user_id == 4:
    user.profile_img = "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668558217/vykblvhfizwomd6fqgzr.png"

elif user.user_id == 5:
    user.profile_img = "https://res.cloudinary.com/lokahi-cloud/image/upload/v1668558257/y1vbha6vo7njtzpduxta.png"    

model.db.session.commit()

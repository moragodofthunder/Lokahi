"""Script to seed database."""

import os
from random import choice, randint, sample
from datetime import datetime

import model
import lokahi_server
import crud

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


#Create 5 fake users
for n in range(5):
    email = f"user{n}@test.com"
    password = "1234"
    get_name = sample(f_names, 1)
    fname = "".join(get_name)
    print(f"THIS IS THE FIRST NAAAAAME: {fname}")
    lname = names[fname]
    profile_img = "/static/img/avatars/purple-profile.png"

    user = crud.create_user(email, password, fname, lname, profile_img)
    model.db.session.add(user)
    model.db.session.commit()

#Give each user 6 fake trips:
    for i in range(6):
        get_city = sample(cities, 1)
        trip_city = "".join(get_city)
        trip_country = places[trip_city]
        random_start = randint(14, 20)
        start_date = f"2022-11-{random_start}"
        random_end = random_start + 5
        end_date = f"2022-11-{random_end}"
        trip_name = f"Trip #{i + 1}: {trip_city}, {trip_country}"
        trip_img = "/static/img/cards/suitcase.png"

        trip = crud.create_trip(trip_name, trip_country, 
        trip_city, start_date, end_date, trip_img, user.user_id)
        model.db.session.add(trip)

model.db.session.commit()

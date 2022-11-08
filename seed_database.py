"""Script to seed database."""

import os
from random import choice, randint
from datetime import datetime

import model
import lokahi_server
import crud

os.system("dropdb lokahi")
os.system("createdb lokahi")

model.connect_to_db(lokahi_server.app)
model.db.create_all()

places = {"Budapest": "Hungary", "Tokyo": "Japan", "Mexico City": "Mexico",
"Gdansk": "Poland", "London": "England", "Honolulu": "United States"}

# res = key, val = random.choice(list(places.items()))

cities = []

cities = list(places.keys())


#Create fake users
for n in range(5):
    email = f"user{n}@test.com"
    password = "1234"
    fname = "Fake"
    lname = f"Human{n}"

    user = crud.create_user(email, password, fname, lname)
    model.db.session.add(user)
    model.db.session.commit()

#Give each user 10 fake trips:
    for i in range(10):
        trip_name = f"Trip # {i}"
        trip_city = choice(cities)
        trip_country = places[trip_city]
        random_date = randint(8, 20)
        start_date = f"2022-11-{random_date}"
        random_end = random_date + 5
        end_date = f"2022-11-{random_end}"

        trip = crud.create_trip(trip_name, trip_city, 
        trip_country, start_date, end_date, user.user_id)
        model.db.session.add(trip)

model.db.session.commit()

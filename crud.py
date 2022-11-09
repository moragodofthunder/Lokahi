"""CRUD operations."""
from model import db, User, Trip, Place, connect_to_db
from _datetime import datetime

###-----------------------------GET-USER-BY-EMAIL-------------------------###
def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


###--------------------------------CREATE-USER----------------------------###
def create_user(email, password, fname, lname):
    """Create and return a new user."""

    user = User(email=email, password=password, fname=fname, lname=lname)

    return user  

###-----------------------------CHECK-EMAIL-AND-PASS----------------------###
def check_email_and_pass(email, password):
    return User.query.filter(User.password == password, 
                            User.email == email).first()


###-----------------------------GET-USER-BY-EMAIL--------------------------###
def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


###-------------------------------GET-USER-BY-ID----------------------------###
def get_user_by_id(user_id):
    return User.query.filter(User.user_id == user_id).first()


###--------------------------------CREATE-TRIP-------------------------------###
def create_trip(trip_name, trip_country, trip_city, start_date, 
                end_date, user_id):
    """Create trip and return trip."""

    trip = Trip(trip_name=trip_name, trip_country=trip_country,
            trip_city=trip_city, start_date=start_date, 
            end_date=end_date, user_id=user_id)

    return trip

###-------------------------------GET-TRIP-BY-ID-----------------------------###
def get_trip_by_id(trip_id):
    return Trip.query.get(trip_id)


###-------------------------------GET-PLACE-BY-ID----------------------------###
def get_place_by_id(place_id):
    return Place.query.get(place_id)


###-----------------------------GET-TRIP-BY-USER-ID--------------------------###
def get_trips_by_user_id(user_id):
    return Trip.query.filter(Trip.user_id == user_id).order_by(Trip.start_date).all()

###-------------------------------SAVE-PLACE-TO-DB----------------------------###
def save_place(user_id, trip_id, ps_name, ps_cat, ps_notes, new_ps_itin, ps_lat, ps_lng, ps_city, ps_country):

    if not new_ps_itin:
        in_itinerary = False
    else:
        in_itinerary = True

    if not ps_notes:
        ps_notes = ""

    saved_place = Place(user_id=user_id, trip_id=trip_id, category=ps_cat, place_name=ps_name, 
    latitude=ps_lat, longitude=ps_lng, in_itinerary=in_itinerary, itinerary_dt=new_ps_itin, place_city = ps_city, 
    place_country = ps_country)

    return saved_place

###-------------------------------GET-PLACE-FROM-DB----------------------------###
# def get_itinerary_activity(trip_id):

#     # trip_id = Place.query.filter(Place.trip_id == trip_id).first()
#     # it_datetime = Place.query.filter(Place.itinerary_dt == it_datetime).first()
#     # name = Place.query.filter(Place.place_name == name).first()

#     activity = Place(trip_id=trip_id, place_name=place_name, itinerary_dt=itinerary_dt)

#     return activity

###-------------------------------GET-PLACES-BY-TRIP----------------------------###
def get_places_by_trip(trip_id):
    return Place.query.filter(Place.trip == trip_id).order_by(Place.itinerary_dt).all()


###---------------------------------OTHER-STUFF-------------------------------###
if __name__ == '__main__':
    from lokahi_server import app
    connect_to_db(app)
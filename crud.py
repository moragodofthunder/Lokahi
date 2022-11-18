"""CRUD operations."""
from model import db, User, Trip, Place, connect_to_db
from _datetime import datetime

###-----------------------------GET-USER-BY-EMAIL-------------------------###
def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


###--------------------------------CREATE-USER----------------------------###
def create_user(email, password, fname, lname, profile_img):
    """Create and return a new user."""

    user = User(email=email, password=password, fname=fname, lname=lname, 
    profile_img=profile_img)

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
                end_date, trip_img, trip_lat, trip_lng, user_id):
    """Create trip and return trip."""

    trip = Trip(trip_name=trip_name, trip_country=trip_country,
            trip_city=trip_city, start_date=start_date, 
            end_date=end_date, trip_img=trip_img, trip_lat=trip_lat,
            trip_lng=trip_lng, user_id=user_id)

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
def save_place(user_id, trip_id, ps_name, ps_cat, ps_notes, in_itinerary, new_ps_itin, ps_lat, ps_lng, ps_city, ps_country,
cat_pin, cat_emoji):

    if not ps_notes:
        ps_notes = ""

    saved_place = Place(user_id=user_id, trip_id=trip_id, category=ps_cat, place_name=ps_name, 
    latitude=ps_lat, longitude=ps_lng, in_itinerary=in_itinerary, itinerary_dt=new_ps_itin, place_city=ps_city, 
    place_country=ps_country, cat_pin=cat_pin, cat_emoji=cat_emoji)

    return saved_place

###-------------------------------GET-FRIEND-BY-EMAIL--------------------------###
def get_friend_by_email(email):
    return User.query.filter(User.email == email).first()

###-----------------------------GET-ALL-FRIENDS-FROM-OHANA---------------------###
def get_all_friends_from_ohana(user_id):
    return User.query.filter(User.user_id == user_id, User.following).order_by(User.following.fname).all()


###-------------------------------GET-PLACES-BY-TRIP----------------------------###
def get_places_by_trip(trip_id):
    return Place.query.filter(Place.trip == trip_id).order_by(Place.itinerary_dt).all()

###-------------------------------GET-PLACES-BY-CATEGORY-------------------------###
def get_places_by_cat(trip_id):
    return Place.query.filter(Place.trip == trip_id).order_by(Place.category).all()

###-------------------------------GET-PLACES-BY-USER-ID------------------------###
def get_places_by_user(user_id):
    return Place.query.filter(Place.user_id == user_id).order_by(Place.place_country).all()

###----------------------------------OTHER-STUFF---------------------------------###
if __name__ == '__main__':
    from lokahi_server import app
    connect_to_db(app)
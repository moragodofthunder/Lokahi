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
def save_place(user_id, trip_id, ps_name, ps_cat, ps_notes, ps_itinerary, ps_lat, ps_lng, ps_city, ps_country):

    if not ps_itinerary:
        in_itinerary = False
    else:
        in_itinerary = True
        ps_itinerary = datetime.strptime(ps_itinerary,'%A, %b %d %Y').strftime('%Y-%m-%d')

    if not ps_notes:
        ps_notes = ""

    saved_place = Place(user_id=user_id, trip_id=trip_id, category=ps_cat, place_name=ps_name, 
    latitude=ps_lat, longitude=ps_lng, in_itinerary=in_itinerary, itinerary_dt=ps_itinerary, place_city = ps_city, 
    place_country = ps_country)

    return saved_place

###-------------------------------GET-PLACE-FROM-DB----------------------------###
def get_places_in_itinerary(itinerary_dt):

    itinerary_dt = Place.query.filter(Place.itinerary_dt == itinerary_dt).order_by(Place.place_id).all()
    places = Place.query.filter(Trip.places).all()
    trip_id = Place.query.filter(Place.trip_id).first()

    if trip_id in places:
        return places



###---------------------------------OTHER-STUFF-------------------------------###
if __name__ == '__main__':
    from lokahi_server import app
    connect_to_db(app)
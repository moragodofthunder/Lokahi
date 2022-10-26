"""CRUD operations."""
from model import db, User, Trip, Place, Activity, connect_to_db

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def create_user(email, password, fname, lname):
    """Create and return a new user."""

    user = User(email=email, password=password, fname=fname, lname=lname)

    return user  

def check_email_and_pass(email, password):
    return User.query.filter(User.password == password, 
                            User.email == email).first()

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

def get_user_by_id(user_id):
    return User.query.filter(User.user_id == user_id).first()

def create_trip(trip_name, trip_country, trip_city, start_date, 
                end_date, user_id):
    """Create trip and return trip."""

    trip = Trip(trip_name=trip_name, trip_country=trip_country,
            trip_city=trip_city, start_date=start_date, 
            end_date=end_date, user_id=user_id)

    return trip

def get_trip_by_id(trip_id):
    return Trip.query.get(trip_id)


if __name__ == '__main__':
    from lokahi_server import app
    connect_to_db(app)
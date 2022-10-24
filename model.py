"""Models for Lokahi web app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User data"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable= False)
    fname = db.Column(db.String(30), nullable= False)
    lname = db.Column(db.String(30), nullable= True)
    email = db.Column(db.String(50), unique= True, nullable= False)
    password = db.Column(db.String, nullable= False)
    profile_img = db.Column(db.String, nullable= True)

    trips = db.relationship("Trip", back_populates="user")
    places = db.relationship("Place", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} fname={self.fname}>"

class Trip(db.Model):
    """Trip data"""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable= False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id")
                        nullable= False)
    trip_name = db.Column(db.String(50), nullable= False)
    trip_country = db.Column(db.String(30), nullable= False)
    trip_city = db.Column(db.String(30), nullable= False)
    start_date = db.Column(db.Date, nullable= False)
    end_date = db.Column(db.Date, nullable= False)
    trip_img = db.Column(db.String, nullable= True)

    user = db.relationship("User", back_populates="trips")
    places = db.relationship("Place", back_populates="trip")
    activities = db.relationship("Trip", back_populates="trip")

    def __repr__(self):
        return f"<Trip trip_id={self.trip_id} trip_name={self.trip_name} trip_city ={self.trip_city}>"

class Place(db.Model):
    """Saved place data"""

    __tablename__ = "places"

    place_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable= False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id")
                        nullable= False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey("trips.trip_id")
                        nullable= False)
    place_name = db.Column(db.String(50), nullable= False)
    place_country = db.Column(db.String(30), nullable= False)
    place_city = db.Column(db.String(30), nullable= False)
    in_itinerary = db.Column(db.Boolean, nullable= False)
    category = db.Column(db.String(30), nullable= False)
    latitude = db.Column(db.Float, nullable= False)
    longitude = db.Column(db.Float, nullable= False)

    user = db.relationship("User", back_populates="places")
    trip = db.relationship("Trip", back_populates="places")
    activity = db.relationship("Activity", uselist= False, back_populates= "place")

    def __repr__(self):
        return f"<Place place_id={self.place_id} place_name={self.place_name}>"

class Activity(db.Model):
    """Activity data"""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable= False)
    place_id = db.Column(db.Integer,
                        db.ForeignKey("places.place_id")
                        nullable= False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey("trips.trip_id")
                        nullable= False)
    activity_datetime = db.Column(db.DateTime)

    place = db.relationship("Place", uselist= False, back_populates="activity")
    trip = db.relationship("Trip", back_populates="activities")

    def __repr__(self):
        return f"<Activity activity_id={self.activity_id} place_name={self.place.place_name}>"



if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
"""Models for Lokahi web app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


###----------------------------USER-CLASS---------------------------###
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


###----------------------------TRIP-CLASS---------------------------###
class Trip(db.Model):
    """Trip data"""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable= False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable= False)
    trip_name = db.Column(db.String(50), nullable= False)
    trip_country = db.Column(db.String(30), nullable= False)
    trip_city = db.Column(db.String(30), nullable= False)
    start_date = db.Column(db.Date, nullable= False)
    end_date = db.Column(db.Date, nullable= False)
    trip_img = db.Column(db.String, nullable= True)

    user = db.relationship("User", back_populates="trips")
    places = db.relationship("Place", back_populates="trip")
    # activities = db.relationship("Activity", back_populates="trip")

    def __repr__(self):
        return f"<Trip trip_id={self.trip_id} trip_name={self.trip_name} trip_city ={self.trip_city}>"


###----------------------------PLACE-CLASS---------------------------###
class Place(db.Model):
    """Saved place data"""

    __tablename__ = "places"

    place_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True,
                        nullable= False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable= False)
    trip_id = db.Column(db.Integer,
                        db.ForeignKey("trips.trip_id"),
                        nullable= False)
    place_name = db.Column(db.String(50), nullable= False)
    place_country = db.Column(db.String(30), nullable= False)
    place_city = db.Column(db.String(30), nullable= False)
    in_itinerary = db.Column(db.Boolean, nullable= False)
    itinerary_dt = db.Column(db.DateTime)
    category = db.Column(db.String(30), nullable= False)
    latitude = db.Column(db.Float, nullable= False)
    longitude = db.Column(db.Float, nullable= False)

    user = db.relationship("User", back_populates="places")
    trip = db.relationship("Trip", back_populates="places")
    # activity = db.relationship("Activity", uselist= False, back_populates= "place")

    def __repr__(self):
        return f"<Place place_id={self.place_id} place_name={self.place_name}>"


# ###-------------------------ACTIVITY-CLASS---------------------------###
# class Activity(db.Model):
#     """Activity data"""

#     __tablename__ = "activities"

#     place_id = db.Column(db.Integer,
#                         db.ForeignKey("places.place_id"), primary_key=True,
#                         nullable= False)
#     trip_id = db.Column(db.Integer,
#                         db.ForeignKey("trips.trip_id"),
#                         nullable= False)
#     activity_datetime = db.Column(db.DateTime)

#     place = db.relationship("Place", uselist= False, back_populates="activity")
#     trip = db.relationship("Trip", back_populates="activities")

#     def __repr__(self):
#         return f"<Activity activity_id={self.activity_id} place_name={self.place.place_name}>"


###---------------------------CONNECT-TO-DB--------------------------###
def connect_to_db(flask_app, db_uri="postgresql:///lokahi", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


###----------------------------SERVER-STUFF--------------------------###
if __name__ == "__main__":
    from lokahi_server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
"""Models for Lokahi web app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

friend = db.Table(
    'friends',
    db.Column('friend_id', db.Integer, primary_key=True),
    db.Column('f1_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('f2_id', db.Integer, db.ForeignKey('users.user_id'))
)

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

    trips = db.relationship("Trip", secondary="trip_users", back_populates="users")
    places = db.relationship("Place", back_populates="user")

    following = db.relationship("User",         
        secondary=friend,
        primaryjoin=user_id == friend.c.f1_id,
        secondaryjoin=user_id == friend.c.f2_id,
        backref='followers'
        )

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
    trip_lat = db.Column(db.String, nullable= True)
    trip_lng = db.Column(db.String, nullable= True)

    users = db.relationship("User", secondary="trip_users", back_populates="trips")
    places = db.relationship("Place", back_populates="trip")

    def __repr__(self):
        return f"<Trip trip_id={self.trip_id} trip_name={self.trip_name} trip_city ={self.trip_city}>"
###----------------------------TRIP-OHANA---------------------------###
class TripUser(db.Model):

    __tablename__ = "trip_users"

    trip_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"), nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable= False)


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
    place_img = db.Column(db.String, nullable=True)
    in_itinerary = db.Column(db.Boolean, nullable= False)
    itinerary_dt = db.Column(db.DateTime)
    category = db.Column(db.String(30), nullable= False)
    cat_pin = db.Column(db.String, nullable=True)
    cat_emoji = db.Column(db.String, nullable=True)
    cat_banner = db.Column(db.String, nullable=True)
    cat_td = db.Column(db.String, nullable=True)
    latitude = db.Column(db.Float, nullable= False)
    longitude = db.Column(db.Float, nullable= False)
    place_notes = db.Column(db.String, nullable=True)

    user = db.relationship("User", back_populates="places")
    trip = db.relationship("Trip", back_populates="places")

    def __repr__(self):
        return f"<Place place_id={self.place_id} place_name={self.place_name}>"



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
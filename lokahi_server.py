"""Server for Lokahi web app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import cowsay
import os
import requests
from datetime import date, timedelta, datetime

app = Flask(__name__)
app.secret_key = os.environ['app_secret_key']
api_key = os.environ['YOUR_API_KEY']
app.jinja_env.undefined = StrictUndefined


###-----------------------------------HOMEPAGE--------------------------------###
@app.route('/')
def homepage():
    """"Return render template to homepage.html"""

    return render_template('homepage.html')


###-----------------------------------LOGIN-PAGE--------------------------------###

@app.route('/login')
def show_login_page():
    """Shows log in and create account page"""

    return render_template('login.html')


###----------------------------WHEN-USER-TRIES-TO-LOGIN-------------------------###
@app.route('/login', methods=['POST'])
def login_user():
    """Login to user account"""

    email = request.form.get("email")
    password = request.form.get("password")

    match = crud.check_email_and_pass(email, password)

    if not match:
        flash("This email doesn't match anything in our system.")
        return redirect("/login")
    else:
        session["user_id"]=match.user_id
        return redirect(f"/user_profile")


###----------------------------LOG-OUT--------------------------------###
@app.route('/logout')
def logout_user():
    """Log out user"""
    
    del session["user_id"]

    flash("A hui hou kākou!")

    return redirect("/login")


###----------------------------USER-PROFILE-----------------------------###
@app.route('/user_profile')
def show_user_profile():
    """Return render template to user_profile.html"""

    if "user_id" in session:
        flash("Aloha 🤙")
        user = crud.get_user_by_id(session["user_id"])
        user_trips = crud.get_trips_by_user_id(user.user_id)

        upcoming = []
        past = []
        for trip in user_trips:
            if trip.start_date >= date.today():
                upcoming.append(trip)
            else:
                past.append(trip)

        return render_template('user_profile.html', first_name=user.fname, 
        user_trips=user_trips, upcoming=upcoming, past=past)

    else:
        flash("Please log in or create new account.")
        return redirect("/login")


###----------------------------ADDING-NEW-USER-TO-DB-------------------------###
@app.route('/user_profile', methods=['POST'])
def create_new_user():
    """Create new user account"""

    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("first-name")
    lname = request.form.get("last-name")

    user = crud.get_user_by_email(email)

    if user:
        flash("An account with this email already exists.")
    else:
        user = crud.create_user(email, password, fname, lname)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.")
    
        return render_template("user_profile.html", first_name=fname)


###-------------------------------NEW-TRIP----------------------------------###
@app.route('/new_trip')
def show_new_trip_form():
    """Show blank new trip form"""

    return render_template("new_trip.html")


###---------------------------ADDING-NEW-TRIP-TO-DB-------------------------###
@app.route('/new_trip', methods=['POST'])
def create_new_trip():
    """Create new trip and route to trip planner"""

    trip_name = request.form.get("trip-name")
    trip_country = request.form.get("trip-country")
    trip_city = request.form.get("trip-city")
    start_date = request.form.get("start-date")
    end_date = request.form.get("end-date")

    trip = crud.create_trip(trip_name, trip_country, trip_city, 
    start_date, end_date, session['user_id'])
    db.session.add(trip)
    db.session.commit()
    
    session['trip_id'] = trip.trip_id

    trip_id = trip.trip_id
    
    return redirect(f"/trip_planner/{trip_id}")


###-------------------TRIP-PLANNER-and-TRAVEL-DATE-LIST----------------###
@app.route('/trip_planner/<trip_id>')
def show_trip_planner_with_trip(trip_id):
    """Return render template to trip_planner.html for specific trip"""

    trip = crud.get_trip_by_id(trip_id)
    start = trip.start_date
    end = trip.end_date
    travel_dates = [start.strftime('%A, %B %d')]

    delta = timedelta(days = 1)
    while start <= end:
        timedelta(days = 1)
        start += delta
        formatted_date = start.strftime('%A, %B %d')
        travel_dates.append(formatted_date)

    travel_dates.pop()
    
    return render_template('trip_planner.html', 
    trip=trip, YOUR_API_KEY=api_key, travel_dates=travel_dates)


###-----------------------------TRIP-DETAILS----------------------------###
@app.route('/trip_details/<trip_id>')
def show_trip_details(trip_id):
    """Return render template to trip_planner.html for specific trip"""

    trip = crud.get_trip_by_id(trip_id)
    activities = trip.activities

    if trip.start_date >= date.today():
        upcoming = True
    else:
        upcoming = False
    
    return render_template('trip_details.html', trip=trip, 
    activities=activities, upcoming=upcoming)


###-----------------------------PLACE-SEARCH----------------------------###
@app.route('/api/place-search')
def get_place_info():
    """Get place info for place user searches for from Places API"""

    user_place = request.args.get('userSearch')
    user_loc = request.args.get('userLocation')

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"

    payload = {
        'location' : user_loc[1:-1],
        'keyword' : f"{user_place}",
        'radius' : 50000,
        'key' : api_key
        }
    headers = {}

    response = requests.get(url, params=payload).json()
    print(jsonify(response))

    #TO SEE ALL JSON OBJECT DATA:
    # return response

    place_data = []

    for item in response["results"]:
        if item["business_status"] == "OPERATIONAL":
            new_place_dict = {}
            new_place_dict['name'] = item.get("name")
            new_place_dict['rating'] = item.get("rating")
            new_place_dict['place_id'] = item.get("place_id")
            new_place_dict['vicinity'] = item.get("vicinity")
            new_place_dict['opening_hours'] = item.get("opening_hours")
            new_place_dict['lat'] = item['geometry']['location']['lat']
            new_place_dict['lng'] = item['geometry']['location']['lng']
            new_place_dict['types'] = item['types'][0]
            if 'photos' in item:
                photo_ref = item['photos'][0]['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={api_key}"
                new_place_dict['photo_url'] = photo_url
            place_data.append(new_place_dict)

    session['ps-lat'] = new_place_dict['lat']
    session['ps-lng'] = new_place_dict['lng']
    session['ps-name'] = new_place_dict['name']
    session['ps-addr'] = new_place_dict['vicinity']


    #Comment out this last line if trying to see all of JSON Object data:
    return jsonify(results=place_data)

@app.route('/save-place', methods=['POST'])
def save_place_data():
    
    ps_cat = request.json["psCategory"]
    ps_notes = request.json["psNotes"]
    ps_itinerary = request.json["psItinerary"]
    ps_city = request.json["psCity"]
    ps_country = request.json["psCountry"]
    trip_id = request.json["psTripId"]

    ps_name = session['ps-name']
    ps_lat = session['ps-lat']
    ps_lng = session['ps-lng']

    user_id = session['user_id']
    

    saved_place = crud.save_place(user_id, trip_id, ps_name, ps_cat, ps_notes, ps_itinerary, ps_lat, 
    ps_lng, ps_city, ps_country)
    db.session.add(saved_place)
    db.session.commit()
    #play with request getting values I want
    #take the psFormInputs and session items and put them in crud function
    #to put in db
    
    #then clear session objects
    #then send back response with success message (in console log)
    #movie rating see "update_ratings" route

    print(saved_place)

    return "Success"

###-----------------------------OTHER-STUFF----------------------------###

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
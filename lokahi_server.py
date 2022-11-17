"""Server for Lokahi web app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import cloudinary.uploader
import cloudinary
import cowsay
import os
import requests
from datetime import date, timedelta, datetime

app = Flask(__name__)
app.secret_key = os.environ['app_secret_key']
api_key = os.environ['YOUR_API_KEY']

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "lokahi-cloud"
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
        flash("Aloha 🤙")
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
        user = crud.get_user_by_id(session["user_id"])
        user_trips = crud.get_trips_by_user_id(user.user_id)

        upcoming = []
        past = []
        for trip in user_trips:
            if trip.start_date >= date.today():
                upcoming.append(trip)
            else:
                past.append(trip)

        return render_template('user_profile.html', user=user, 
        user_trips=user_trips, upcoming=upcoming, past=past)

    else:
        flash("Please log in or create new account.")
        return redirect("/login")

###----------------------------USER-PROFILE-PIC----------------------------###
@app.route('/api/profile_img', methods=['POST'])
def upload_profile_img():
    """Let users upload a photo for their profile image"""

    profile_img = request.files['profile-img']

    result = cloudinary.uploader.upload(profile_img, api_key=CLOUDINARY_KEY,
    api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME, gravity="auto", 
    height=200, width=200, crop="fill")

    img_url = result['secure_url']

    user = crud.get_user_by_id(session["user_id"])
    user.profile_img = img_url
    db.session.commit()

    flash("Profile image changed")

    return redirect("/user_profile")


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

 ###---------------------------ADDING-FRIEND-TO-DB---------------------------###
@app.route('/find_friends', methods=['POST'])
def find_friends_of_user():

    user = crud.get_user_by_id(session["user_id"])

    friend_email = request.form.get("friend-search")
    friend_user = crud.get_friend_by_email(friend_email)

    if friend_user:
        user.following.append(friend_user)
        db.session.add(friend_user)
        db.session.commit()
        flash(f"{friend_user.fname} added to your Travel 'Ohana")
    else:
        flash("User not found")

    return redirect("/user_profile")

###---------------------------ADDING-FRIEND-TO-TRIP--------------------------###
@app.route('/add_friends_to_trip/<trip_id>', methods=['POST'])
def add_friends_to_trip(trip_id):

    user = crud.get_user_by_id(session["user_id"])
    trip_bud = request.form.get("trip-buds")
    trip_friend = crud.get_user_by_id(int(trip_bud))
    trip = crud.get_trip_by_id(trip_id)

    trip.users.append(trip_friend)
    db.session.add(trip)
    db.session.commit()
    flash(f"{trip_friend.fname} was added to your 'Ohana Traveling Lōkahi")

    return redirect(f"/trip_details/{trip_id}")


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
    trip_img = "/static/img/cards/suitcase.png"

    address = f"{trip_city}, {trip_country}"
    api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
    api_response_dict = api_response.json()

    if api_response_dict['status'] == 'OK':
        trip_lat = api_response_dict['results'][0]['geometry']['location']['lat']
        trip_lng = api_response_dict['results'][0]['geometry']['location']['lng']

    trip = crud.create_trip(trip_name, trip_country, trip_city, 
    start_date, end_date, trip_img, trip_lat, trip_lng, session['user_id'])

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
    travel_dates = [start.strftime('%A, %b %d %Y')]

    delta = timedelta(days = 1)
    while start <= end:
        timedelta(days = 1)
        start += delta
        formatted_date = start.strftime('%A, %b %d %Y')
        travel_dates.append(formatted_date)

    travel_dates.pop()
    
    return render_template('trip_planner.html', 
    trip=trip, YOUR_API_KEY=api_key, travel_dates=travel_dates)


###-----------------------------TRIP-DETAILS----------------------------###
@app.route('/trip_details/<trip_id>')
def show_trip_details(trip_id):
    """Return render template to trip_planner.html for specific trip"""

    trip = crud.get_trip_by_id(trip_id)
    start = trip.start_date
    end = trip.end_date
    travel_dates = [start.strftime('%A, %b %d %Y')]
    unformat_dates = [start]

    delta = timedelta(days = 1)
    while start <= end:
        timedelta(days = 1)
        start += delta
        formatted_date = start.strftime('%A, %b %d %Y')
        unformat_date = start
        travel_dates.append(formatted_date)
        unformat_dates.append(unformat_date)

    travel_dates.pop()
    unformat_dates.pop()

    if start >= date.today():
        upcoming = True
    else:
        upcoming = False

    places_by_trip = crud.get_places_by_trip(trip)
    places_by_cat = crud.get_places_by_cat(trip)

    places_by_day= {}
    places_by_category= {}

    for place in places_by_trip:
        new_dt = place.itinerary_dt.strftime('%A, %b %d %Y')
        if new_dt in places_by_day:
            places_by_day[new_dt].append(place)
        else:
            places_by_day[new_dt] = [place]
    
    for place in places_by_cat:
        category = place.category
        if category in places_by_category:
            places_by_category[category].append(place)
        else:
            places_by_category[category] = [place]

    user = crud.get_user_by_id(session["user_id"])
    
    return render_template('trip_details.html', trip=trip, 
    upcoming=upcoming, travel_dates=travel_dates, 
    places_by_day=places_by_day, places_by_category=places_by_category,
    user=user)


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


###-----------------------------SAVE-PLACE-TO-DB----------------------------###
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

    new_ps_itin = datetime.strptime(ps_itinerary,'%A, %b %d %Y')
    new_ps_itin = new_ps_itin.strftime('%Y-%m-%d')
    
    saved_place = crud.save_place(user_id, trip_id, ps_name, ps_cat, ps_notes, 
    new_ps_itin, ps_lat, ps_lng, ps_city, ps_country)
    db.session.add(saved_place)
    db.session.commit()

    return "Success"
###---------------------------ALL-SAVED-PLACES-----------------------###
@app.route("/api/all_places")
def places_info():
    """JSON info about user's saved places"""

    user = crud.get_user_by_id(session["user_id"])
    # trip = crud.get_trip_by_id(trip_id)
    places = crud.get_places_by_user(user.user_id)
    # trip_places = crud.get_places_by_trip(trip)

    all_places = []

    for place in places:
    
        all_places.append({"id": place.place_id,
        "user": place.user_id,
        "trip": place.trip_id,
        "name": place.place_name,
        "placeCountry": place.place_country,
        "placeCity": place.place_city,
        "inItin": place.in_itinerary,
        "itinDT": place.itinerary_dt,
        "category": place.category,
        "placeLat": place.latitude,
        "placeLng": place.longitude,})
        

    return jsonify(all_places)

###---------------------------MAP-OF-SAVED-PLACES-----------------------###
@app.route("/saved_places_map/<trip_id>")
def show_sp_map(trip_id):
    """Shows map of places user has saved for trip"""

    trip = crud.get_trip_by_id(trip_id)

    if trip.start_date >= date.today():
        upcoming = True
    else:
        upcoming = False

    return render_template("saved_places_map.html", trip=trip, 
    upcoming=upcoming, YOUR_API_KEY=api_key)

###-----------------------------OTHER-STUFF----------------------------###

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
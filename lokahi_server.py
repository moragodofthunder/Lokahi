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
        shared_trips = user.trips

        shared_upcoming = []
        shared_past = []
        upcoming = []
        past = []

        for trip in user_trips:
            if trip.start_date >= date.today():
                upcoming.append(trip)
            else:
                past.append(trip)

        for trip in shared_trips:
            if trip.start_date >= date.today():
                shared_upcoming.append(trip)
            else:
                shared_past.append(trip)

        return render_template('user_profile.html', user=user, 
        user_trips=user_trips, upcoming=upcoming, past=past, 
        shared_upcoming=shared_upcoming, shared_past=shared_past)

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
    banners_by_cat = {}

    for place in places_by_trip:
        if place.itinerary_dt == None:
            continue
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
    trip_maker = crud.get_user_by_id(trip.user_id)
    
    return render_template('trip_details.html', trip=trip, 
    upcoming=upcoming, travel_dates=travel_dates, 
    places_by_day=places_by_day, places_by_category=places_by_category,
    user=user, trip_maker=trip_maker)

###----------------------------USER-TRIP-IMG---------------------------###
@app.route('/api/trip_img/<trip_id>', methods=['POST'])
def upload_trip_img(trip_id):
    """Let users upload a photo for their profile image"""

    trip_img = request.files['trip-img']

    result = cloudinary.uploader.upload(trip_img, api_key=CLOUDINARY_KEY,
    api_secret=CLOUDINARY_SECRET, cloud_name=CLOUD_NAME, gravity="auto", 
    height=300, width=300, crop="fill")

    img_url = result['secure_url']

    trip = crud.get_trip_by_id(trip_id)
    trip.trip_img = img_url
    db.session.commit()

    flash("Trip image changed")

    return redirect(f"/trip_details/{trip_id}")

###---------------------------ITINERARY-EDITOR--------------------------###
@app.route('/itinerary_editor/<trip_id>')
def edit_itinerary(trip_id):
    """Let's users edit itinerary on page"""

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

    places_by_trip = crud.get_places_by_trip(trip)
    places_by_day= {}

    for place in places_by_trip:
        if place.itinerary_dt == None:
            continue
        new_dt = place.itinerary_dt.strftime('%A, %b %d %Y')
        if new_dt in places_by_day:
            places_by_day[new_dt].append(place)
        else:
            places_by_day[new_dt] = [place]

    return render_template("edit-itin.html", trip=trip, travel_dates=travel_dates, 
    places_by_day=places_by_day)


###-----------------------------PLACE-SEARCH----------------------------###
@app.route('/api/place-search')
def get_place_info():
    """Get place info for place user searches for from Places API"""

    user_place = request.args.get('userSearch')
    user_loc = request.args.get('tripLocation')

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

    place_pins = {
    'Breakfast': '/static/img/pins/1-breakfast-pin.png',
    'Lunch': '/static/img/pins/2-lunch-pin.png',
    'Dinner': '/static/img/pins/3-dinner-pin.png',
    'Streetfood': '/static/img/pins/4-streetfood-pin.png',
    'Dessert': '/static/img/pins/5-dessert-pin.png',
    'Cafe': '/static/img/pins/6-cafe-pin.png',
    'Nightlife': '/static/img/pins/7-nightlife-pin.png',
    'Bar/Pub': '/static/img/pins/8-bar-pin.png',
    'Shopping': '/static/img/pins/9-shopping-pin.png',
    'Groceries': '/static/img/pins/10-grocery-pin.png',
    'Convenience Store': '/static/img/pins/11-kombini-pin.png',
    'Outdoor Market': '/static/img/pins/12-farmers-market-pin.png',
    'Covered Market': '/static/img/pins/13-bazaar-pin.png',
    'Bookstore/Library': '/static/img/pins/14-bookstore-pin.png',
    'Train Station': '/static/img/pins/15-train-pin.png',
    'Museum': '/static/img/pins/16-museum-pin.png',
    'Landmark': '/static/img/pins/17-landmark-pin.png',
    'Photo Spot': '/static/img/pins/18-photo-pin.png',
    'Temple/Shrine/Worship': '/static/img/pins/19-shrine-pin.png',
    'Entertainment': '/static/img/pins/20-entertain-pin.png',
    'Music': '/static/img/pins/21-music-pin.png',
    'Hot Spring': '/static/img/pins/22-onsen-pin.png',
    'Beach': '/static/img/pins/23-beach-pin.png',
    'Park': '/static/img/pins/24-park-pin.png',
    'Hiking': '/static/img/pins/25-hiking-pin.png',
    'Surfing': '/static/img/pins/26-surf-pin.png',
    'Workspace': '/static/img/pins/27-work-pin.png',
    'COVID Testing': '/static/img/pins/28-covid-pin.png',
    'Miscellaneous': '/static/img/pins/29-misc-pin.png'}

    cat_emojis = {
    'Breakfast': '/static/img/emojis/1-breakfast-emoji.png',
    'Lunch': '/static/img/emojis/2-lunch-emoji.png',
    'Dinner': '/static/img/emojis/3-dinner-emoji.png',
    'Streetfood': '/static/img/emojis/4-streetfood-emoji.png',
    'Dessert': '/static/img/emojis/5-dessert-emoji.png',
    'Cafe': '/static/img/emojis/6-cafe-emoji.png',
    'Nightlife': '/static/img/emojis/7-nightlife-emoji.png',
    'Bar/Pub': '/static/img/emojis/8-bar-emoji.png',
    'Shopping': '/static/img/emojis/9-shopping-emoji.png',
    'Groceries': '/static/img/emojis/10-grocery-emoji.png',
    'Convenience Store': '/static/img/emojis/11-kombini-emoji.png',
    'Outdoor Market': '/static/img/emojis/12-farmers-market-emoji.png',
    'Covered Market': '/static/img/emojis/13-bazaar-emoji.png',
    'Bookstore/Library': '/static/img/emojis/14-bookstore-emoji.png',
    'Train Station': '/static/img/emojis/15-train-emoji.png',
    'Museum': '/static/img/emojis/16-museum-emoji.png',
    'Landmark': '/static/img/emojis/17-landmark-emoji.png',
    'Photo Spot': '/static/img/emojis/18-photo-emoji.png',
    'Temple/Shrine/Worship': '/static/img/emojis/19-shrine-emoji.png',
    'Entertainment': '/static/img/emojis/20-entertain-emoji.png',
    'Music': '/static/img/pins/21-music-pin.png',
    'Hot Spring': '/static/img/emojis/22-onsen-emoji.png',
    'Beach': '/static/img/emojis/23-beach-emoji.png',
    'Park': '/static/img/emojis/24-park-emoji.png',
    'Hiking': '/static/img/emojis/25-hiking-emoji.png',
    'Surfing': '/static/img/emojis/26-surf-emoji.png',
    'Workspace': '/static/img/emojis/27-work-emoji.png',
    'COVID Testing': '/static/img/emojis/28-covid-emoji.png',
    'Miscellaneous': '/static/img/emojis/29-misc-emoji.png'}

    cat_banners = {
    'Breakfast': '/static/img/cat_banners/1-breakfast-banner.png',
    'Lunch': '/static/img/cat_banners/2-lunch-banner.png',
    'Dinner': '/static/img/cat_banners/3-dinner-banner.png',
    'Streetfood': '/static/img/cat_banners/4-streetfood-banner.png',
    'Dessert': '/static/img/cat_banners/5-dessert-banner.png',
    'Cafe': '/static/img/cat_banners/6-cafe-banner.png',
    'Nightlife': '/static/img/cat_banners/7-nightlife-banner.png',
    'Bar/Pub': '/static/img/cat_banners/8-bar-banner.png',
    'Shopping': '/static/img/cat_banners/9-shopping-banner.png',
    'Groceries': '/static/img/cat_banners/10-grocery-banner.png',
    'Convenience Store': '/static/img/cat_banners/11-kombini-banner.png',
    'Outdoor Market': '/static/img/cat_banners/12-farmers-market-banner.png',
    'Covered Market': '/static/img/cat_banners/13-bazaar-banner.png',
    'Bookstore/Library': '/static/img/cat_banners/14-bookstore-banner.png',
    'Train Station': '/static/img/cat_banners/15-train-banner.png',
    'Museum': '/static/img/cat_banners/16-museum-banner.png',
    'Landmark': '/static/img/cat_banners/17-landmark-banner.png',
    'Photo Spot': '/static/img/cat_banners/18-photo-banner.png',
    'Temple/Shrine/Worship': '/static/img/cat_banners/19-shrine-banner.png',
    'Entertainment': '/static/img/cat_banners/20-entertain-banner.png',
    'Music': '/static/img/cat_banners/21-music-banner.png',
    'Hot Spring': '/static/img/cat_banners/22-onsen-banner.png',
    'Beach': '/static/img/cat_banners/23-beach-banner.png',
    'Park': '/static/img/cat_banners/24-park-banner.png',
    'Hiking': '/static/img/cat_banners/25-hiking-banner.png',
    'Surfing': '/static/img/cat_banners/26-surf-banner.png',
    'Workspace': '/static/img/cat_banners/27-work-banner.png',
    'COVID Testing': '/static/img/cat_banners/28-covid-banner.png',
    'Miscellaneous': '/static/img/cat_banners/29-misc-banner.png'
    }

    cat_tds = {
    'Breakfast': '/static/img/cat_td/1-breakfast-td.png',
    'Lunch': '/static/img/cat_td/2-lunch-td.png',
    'Dinner': '/static/img/cat_td/3-dinner-td.png',
    'Streetfood': '/static/img/cat_td/4-streetfood-td.png',
    'Dessert': '/static/img/cat_td/5-dessert-td.png',
    'Cafe': '/static/img/cat_td/6-cafe-td.png',
    'Nightlife': '/static/img/cat_td/7-nightlife-td.png',
    'Bar/Pub': '/static/img/cat_td/8-bar-td.png',
    'Shopping': '/static/img/cat_td/9-shopping-td.png',
    'Groceries': '/static/img/cat_td/10-grocery-td.png',
    'Convenience Store': '/static/img/cat_td/11-kombini-td.png',
    'Outdoor Market': '/static/img/cat_td/12-farmers-market-td.png',
    'Covered Market': '/static/img/cat_td/13-bazaar-td.png',
    'Bookstore/Library': '/static/img/cat_td/14-bookstore-td.png',
    'Train Station': '/static/img/cat_td/15-train-td.png',
    'Museum': '/static/img/cat_td/16-museum-td.png',
    'Landmark': '/static/img/cat_td/17-landmark-td.png',
    'Photo Spot': '/static/img/cat_td/18-photo-td.png',
    'Temple/Shrine/Worship': '/static/img/cat_td/19-shrine-td.png',
    'Entertainment': '/static/img/cat_td/20-entertain-td.png',
    'Music': '/static/img/cat_td/21-music-td.png',
    'Hot Spring': '/static/img/cat_td/22-onsen-td.png',
    'Beach': '/static/img/cat_td/23-beach-td.png',
    'Park': '/static/img/cat_td/24-park-td.png',
    'Hiking': '/static/img/cat_td/25-hiking-td.png',
    'Surfing': '/static/img/cat_td/26-surf-td.png',
    'Workspace': '/static/img/cat_td/27-work-td.png',
    'COVID Testing': '/static/img/cat_td/28-covid-td.png',
    'Miscellaneous': '/static/img/cat_td/29-misc-td.png'  
    }
    
    ps_cat = request.json["psCategory"]
    ps_notes = request.json["psNotes"]
    ps_itinerary = request.json["psItinerary"]
    print(f"THIS IS PS_ITINERARYYYYYYY: {type(ps_itinerary)}")
    ps_city = request.json["psCity"]
    ps_country = request.json["psCountry"]
    trip_id = request.json["psTripId"]
    trip_id = int(trip_id)

    ps_name = session['ps-name']
    ps_lat = session['ps-lat']
    ps_lng = session['ps-lng']
    # place_img = session['place-img']

    cat_pin = place_pins[ps_cat]
    cat_emoji = cat_emojis[ps_cat]
    cat_banner = cat_banners[ps_cat]
    cat_td = cat_tds[ps_cat]

    user_id = session['user_id']

    if ps_itinerary == "":
        new_ps_itin = None
        in_itinerary = False
    else:
        new_ps_itin = datetime.strptime(ps_itinerary,'%A, %b %d %Y')
        new_ps_itin = new_ps_itin.strftime('%Y-%m-%d')
        in_itinerary = True
    
    saved_place = crud.save_place(user_id, trip_id, ps_name, ps_cat, ps_notes, in_itinerary,
    new_ps_itin, ps_lat, ps_lng, ps_city, ps_country, cat_pin, cat_emoji, cat_banner,
    cat_td)
    db.session.add(saved_place)
    db.session.commit()
    flash(f"{ps_name} saved")

    if new_ps_itin is not None:
        flash(f"{ps_name} saved to your itinerary for {ps_itinerary}")

    return "Success"
###---------------------------ALL-SAVED-PLACES-----------------------###
@app.route("/api/all_places/<trip_id>")
def places_info(trip_id):
    """JSON info about user's saved places"""

    trip = crud.get_trip_by_id(int(trip_id))
    places = crud.get_all_places_by_trip(int(trip.trip_id))

    all_places = []

    for place in places:

        if place.in_itinerary == True:
            # place.in_itinerary = "Yes"
            place.itinerary_dt = place.itinerary_dt.strftime('%b %d, %Y')
        else:
            # place.in_itinerary = "No"
            place.itinerary_dt = "N/A"
    
        all_places.append({
        "id": place.place_id,
        "user": place.user_id,
        "trip": place.trip_id,
        "name": place.place_name,
        "placeCountry": place.place_country,
        "placeCity": place.place_city,
        "inItin": place.in_itinerary,
        "itinDT": place.itinerary_dt,
        "category": place.category,
        "catPin": place.cat_pin,
        "catEmoji": place.cat_emoji,
        "placeLat": place.latitude,
        "placeLng": place.longitude,
        "userName": place.user.fname,
        "userImg": place.user.profile_img})
        

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
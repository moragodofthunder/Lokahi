"""Server for Lokahi web app."""
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import cowsay
import os

app = Flask(__name__)
app.secret_key = os.environ['app_secret_key']
api_key = os.environ['YOUR_API_KEY']
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """"Return render template to homepage.html"""

    return render_template('homepage.html')


@app.route('/login')
def show_login_page():
    """Shows log in and create account page"""

    return render_template('login.html')


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
        return redirect(f"/user_profile/{match.user_id}")


@app.route('/user_profile/<user_id>')
def show_user_profile(user_id):
    """Return render template to user_profile.html"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_profile.html', first_name=user.fname)


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


@app.route('/new_trip')
def show_new_trip_form():
    """Show blank new trip form"""
    return render_template("new_trip.html")


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

# @app.route('/trip_planner', methods=['POST'])
# def show_trip_planner():
#     """Return render template for blank_trip_planner.html 
#     without specific trip"""

#     return render_template('blank_trip_planner.html')

@app.route('/trip_planner/<trip_id>')
def show_trip_planner_with_trip(trip_id):
    """Return render template to trip_planner.html for specific trip"""

    trip = crud.get_trip_by_id(trip_id)
    trip_name = trip.trip_name
    trip_city = trip.trip_city
    trip_country = trip.trip_country
    start_date = trip.start_date
    end_date = trip.end_date
    
    return render_template('trip_planner.html', 
    trip_name=trip_name, trip_city=trip_city,
    trip_country=trip_country, start_date=start_date,
    end_date=end_date, YOUR_API_KEY=api_key)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
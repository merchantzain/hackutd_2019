# import libraries
from flask import Flask, render_template, request, redirect, url_for, flash
import amadeus_api
from forms import RegistrationForm
import sqlite3
from db_funcs import *
from datetime import datetime, timedelta
import message as msg

# create flask web application object (instantiated by your WSGI)
app = Flask(__name__)

# todo: user this later to configure application options
app.config["SECRET_KEY"] = "ba01ca77563d9ef068b2fa30392dad35" #random 32 char secret key 

@app.route("/", methods=["GET", "POST"])
def index():
    # use registration form template
    form = RegistrationForm()

    # validate the form inputs and redirect to homepage (index) on success
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        university = form.university.data
        budget = form.budget.data
        weekend = closest_friday(str(form.weekend.data))
        interests = form.interests.data
        post_received(name, email, phone, budget, weekend, interests, university)
        return redirect(url_for("success"))

    return render_template("index.html", form=form)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/alexa/<name>/<email>/<phone>/<budget>/<weekend>")
def alexa(name, email, phone, budget, weekend):
    university = "UT Dallas"
    interests = ""
    weekend = closest_friday(str(weekend))
    post_received(name, email, phone, budget, weekend, interests, university)
    return "done", 200

@app.route("/droptable")
def drop():
    try:
        drop_table()
    except:
        return "drop failed, no table", 200
    return "table dropped", 200

@app.route("/table_status")
def status():
    return str(table_status()), 200

def post_received(name, email, phone, budget, weekend, interests, university):
    current_traveller = [name, email, phone, budget, weekend, interests, university]

    # check if table exists, create otherwise
    create_table()

    # add data to table
    insert_traveler(name, email, phone, university, budget, weekend, interests)

    # get a group of travelers with similar dates, if possible
    group_made, travel_group, common_interests, budget = get_similar_travellers(current_traveller)
    if not group_made:
        return
        
    # book trip
    itinerary = amadeus_api.get_flight(budget=budget, departure_date=travel_group[0][-2])
    if itinerary is None:
        print("No itinerary")
        return

    # twillio to group of followers
    messaged_people = []
    for person in travel_group:
        messaged_people.append([person[1], person[3]])
    msg.send_to_group(messaged_people, itinerary, common_interests)

    # delete travellers from table
    for person in travel_group:
        delete_travellers(person[0])
    print("people deleted")

    return

def closest_friday(day):
    # get closest friday to date
    day = datetime.strptime(day, "%Y-%m-%d")
    while day.weekday() > 4:
        day -= timedelta(1)
    while day.weekday() < 4:
        day += timedelta(1)
    return day.strftime("%Y-%m-%d")

# call upon program startup
if __name__ == '__main__':
    # spawn flask server (in debug mode)
    app.run(debug=True, host='0.0.0.0', port=8001)#, ssl_context='adhoc')
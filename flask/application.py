# import libraries
from flask import Flask, render_template, request
import amadeus_api

# create flask web application object (instantiated by your WSGI)
app = Flask(__name__)

@app.route("/")
def index():
    nearby_airports = amadeus_api.get_nearby_airports()
    out = ""
    for airport in nearby_airports:
        out = out + ", ".join(airport.values()) + "<br/>"
    return amadeus_api.get_flight(), 200

# call upon program startup
if __name__ == '__main__':
    # spawn flask server (in debug mode)
    app.run(debug=True, host='0.0.0.0', port=8001)#, ssl_context='adhoc')
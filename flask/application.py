# import libraries
from flask import Flask, render_template, request
from amadeus import *

# create flask web application object (instantiated by your WSGI)
app = Flask(__name__)

@app.route("/")
def index():
    ip_addr = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    return "Your IP address is: " + ip_addr, 200

# call upon program startup
if __name__ == '__main__':
    # spawn flask server (in debug mode)
    app.run(debug=True, host='0.0.0.0', port=8001, ssl_context='adhoc')
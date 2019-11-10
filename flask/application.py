# import libraries
from flask import Flask, render_template, request, redirect, url_for, flash
import amadeus_api
from forms import RegistrationForm

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
        flash(f"Submitted GTFO Request!", "success")
        return redirect(url_for("index"))

    return render_template("index.html", form=form)

# call upon program startup
if __name__ == '__main__':
    # spawn flask server (in debug mode)
    app.run(debug=True, host='0.0.0.0', port=8001)#, ssl_context='adhoc')
# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse



app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_menu():
    bob = ["bob","9182838282","London","Monday"]
    joe = ["joe","1298713278","London","Monday"]
    billy = ["billy","1238472018","London","Tuesday"]
    people = [bob, joe, billy]
    person = ["ben", "129381729382", "London", "12-08-2019", "$500", "DFW", "12-12-2019", "being a GAMER"]
    #Get the message
    body = request.values.get('Body', None)

    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()


    # Add a message-
    if body == 'Trip Details':
        resp.message(trip_details(person,people))
    else:
        resp.message("Piss off! Thanks so much for your message.")

    return str(resp)

def trip_details(person, people):
    response_string = "Howdy pardner! You are going to " + person[2] + " on " + person[3] + " with "
    peoplecount = 0
    for x in people:
        if x[2] == person[2]:
            if x[3] == person[3]:
                response_string = response_string + x[0] + "(" + x[1] + ") "
                peoplecount = peoplecount + 1
    if peoplecount == 0:
        response_string = response_string + "nobody"
    response_string = response_string + " with a " + person[4] + " ticket from " + person[5] + " and coming back on " + person[6] + ". If you're wondering what to do, you all like " + person[7]
    return response_string

if __name__ == "__main__":
    app.run(debug=True)

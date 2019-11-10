# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
# As said above, this is insecure. In a production environment, these variables would be hidden
account_sid = 'ACb249d5d45a184e6275ddd67f2a81869a'
auth_token = '8efcad633760dd3d35889829a83e7562'
client = Client(account_sid, auth_token)
#This function will construct the message sent to the people in a group, using their interests and itinerary
def send_to_group(people, itin, interests):
    resp_string = "You are going on a trip with "
    for person in people:
        resp_string = resp_string + person[0] + "(" + person[1] + ") "
    resp_string = resp_string + "to " + itin["outgoing"]["destination"] + " on " + itin["outgoing"]["departure_datetime"] + ". Your flight number is " + itin["outgoing"]["airline"] + itin["outgoing"]["flight_number"]
    resp_string = resp_string + " from terminal " + itin["outgoing"]["origin_terminal"] + " in " + itin["outgoing"]["origin"]
    resp_string = resp_string + ". You will arive on " + itin["outgoing"]["destination_datetime"]
    resp_string = resp_string + ". Some common interests between y'all are "
    for inter in interests:
        resp_string = resp_string + inter + ", "
    resp_string = resp_string + "and maybe more!"
    resp_string = resp_string + " You'll be going home on " + itin["arrival"]["departure_datetime"] + " on flight " + itin["arrival"]["airline"]+ itin["arrival"]["flight_number"] + " Have Fun!"
    for person in people:
        send_msg(person[1],resp_string)
    

def send_msg(number,resp_string):
    number = "+1" + number
    message = client.messages \
                    .create(
                        body=resp_string,
                        from_='+13176081989',
                        to=number
                    )

    print(message.sid)

"""
if(__name__=="__main__"):
    people = [['bob',"8323448497"],['joe','8328753755']]
    flight_itinerary = {
        "outgoing":{
            "origin":'DFW',
            "airline":'AA',
            "origin_terminal":'E',
            "departure_datetime":'12-01-19',
            "destination":'London',
            "destination_datetime":'12-02-19',
            "flight_number":'99'
        },
        "arrival":{
            "origin":'Heathrow',
            "airline":'AA',
            "departure_datetime":'12-04-19',
            "destination":'Dallas',
            "destination_datetime":'12-05-19',
            "flight_number":'69'
        },
        "cost":'$420'
    }
    interests = ["gamer", "bars", "drink"]
    send_to_group(people, flight_itinerary, interests)
"""
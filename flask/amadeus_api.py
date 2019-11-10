#import libraries
from amadeus import Client, ResponseError
import requests
import json
from datetime import datetime, timedelta
import random

# api keys and login client initialization
api_key = "vu33j2BKo1CqkOl6GJzcAVbLIJb6KTp1"
api_secret = "F2W2mKCHRyoPJQgn"
amadeus = Client(client_id=api_key, client_secret=api_secret)

# get api token
def get_token():
    # make post request to get api bearer token
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = f"grant_type=client_credentials&client_id={api_key}&client_secret={api_secret}"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "test.api.amadeus.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "103",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    
    # parse response and return token
    token = json.loads(response.text)["access_token"]
    return token

# get 3 closest airports (default to utd's location)
def get_nearby_airports(lat=32.985764, lon=-96.750099, token=get_token()):
    # make get request to get nearest airports based on coordinates
    url = "https://test.api.amadeus.com/v1/reference-data/locations/airports"
    querystring = {"latitude":str(lat), "longitude":str(lon), "radius":str(75), "sort":"distance"}
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "test.api.amadeus.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    # get reponse and parse as json
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)["data"]
    
    # return 3 closest airports' names, iata codes, city names, city iata codes, and distance
    nearby_airports = []
    for airport in data[:3]:
        nearby_airports.append(
            {
                "airport_name":airport["name"],
                "airport_iat":airport["iataCode"],
                "airport_city":airport["address"]["cityName"],
                "airport_citycode":airport["address"]["cityCode"],
                "airport_dist":str(airport["distance"]["value"])
            })
    return nearby_airports

# take a group's budget and deadline, return 3 cities to fly to and corresponding flights
def get_flight(budget=300, departure_date="2019-11-15", token=get_token()):
    # get closest friday to date
    departure_date = datetime.strptime(departure_date, "%Y-%m-%d")
    while departure_date.weekday() > 4:
        departure_date -= timedelta(1)
    while departure_date.weekday() < 4:
        departure_date += timedelta(1)
    return_date = departure_date + timedelta(3)
    departure_date = departure_date.strftime("%Y-%m-%d")
    return_date = return_date.strftime("%Y-%m-%d")

    # get IATA code of your closest airport's cities
    try:
        city_codes = []
        for airport in get_nearby_airports(token=token):
            city = airport["airport_citycode"]
            if city not in city_codes:
                city_codes.append(city)
    except:
        return None

    # loop over closest city's airport's and get a random destination within budget
    random_trip = []
    for city_code in city_codes:
        # get a random flight out of here within budget
        url = "https://test.api.amadeus.com/v1/shopping/flight-destinations"
        querystring = { "origin":city_code,
                        "departureDate":departure_date,
                        "oneWay":"false",
                        "duration":"3",
                        "nonStop":"false",
                        "maxPrice":str(budget),
                        "viewBy":"DESTINATION"
                    }
        headers = { 'Authorization': f"Bearer {token}",
                    'Accept': "*/*",
                    'Cache-Control': "no-cache",
                    'Host': "test.api.amadeus.com",
                    'Accept-Encoding': "gzip, deflate",
                    'Connection': "keep-alive",
                    'cache-control': "no-cache"
                }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)
        try:
            for index in random.sample(range(0, len(response["data"]) - 1), 1):
                random_trip.append([response["data"][index]["origin"], response["data"][index]["destination"]])
        except:
            pass

    if len(random_trip) < 1:
        return None
    
    try:
        # get flight itinerary for trip
        url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        querystring = {
                    "originLocationCode":random_trip[0][0],
                    "destinationLocationCode":random_trip[0][1],
                    "departureDate":departure_date,
                    "returnDate":return_date,
                    "adults":"1",
                    "nonStop":"false",
                    "currencyCode":"USD",
                    "max":"1"}
        headers = {
                    'Authorization': f"Bearer {token}",
                    'Accept': "*/*",
                    'Cache-Control': "no-cache",
                    'Host': "test.api.amadeus.com",
                    'Accept-Encoding': "gzip, deflate",
                    'Connection': "keep-alive",
                    'cache-control': "no-cache"
                }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = json.loads(response.text)

        flight_itinerary = {
            "outgoing":{
                "origin":response["data"][0]["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                "origin_terminal":response["data"][0]["itineraries"][0]["segments"][0]["departure"]["terminal"],
                "departure_datetime":response["data"][0]["itineraries"][0]["segments"][0]["departure"]["at"],
                "destination":response["data"][0]["itineraries"][0]["segments"][0]["arrival"]["iataCode"],
                "destination_datetime":response["data"][0]["itineraries"][0]["segments"][0]["arrival"]["at"],
                "airline":response["data"][0]["itineraries"][0]["segments"][0]["carrierCode"],
                "itinerary_code":response["data"][0]["itineraries"][0]["segments"][0]["duration"],
                "flight_number":response["data"][0]["itineraries"][0]["segments"][0]["number"]
            },
            "arrival":{
                "origin":response["data"][0]["itineraries"][1]["segments"][0]["departure"]["iataCode"],
                "departure_datetime":response["data"][0]["itineraries"][1]["segments"][0]["departure"]["at"],
                "destination":response["data"][0]["itineraries"][1]["segments"][0]["arrival"]["iataCode"],
                "destination_terminal":response["data"][0]["itineraries"][1]["segments"][0]["arrival"]["terminal"],
                "destination_datetime":response["data"][0]["itineraries"][1]["segments"][0]["arrival"]["at"],
                "airline":response["data"][0]["itineraries"][1]["segments"][0]["carrierCode"],
                "itinerary_code":response["data"][0]["itineraries"][1]["segments"][0]["duration"],
                "flight_number":response["data"][0]["itineraries"][1]["segments"][0]["number"]
            },
            "cost":response["data"][0]["price"]["base"]
        }

        # return flight locations, flight numbers, costs, and dates
        return flight_itinerary
    except:
        print("Some fucking error")
        return None

# get cheap hotels for location
# get attractions for location

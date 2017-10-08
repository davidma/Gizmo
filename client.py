import os
import sys
import apiai
import uuid
import json
import pyowm

APIAI_CLIENT_TOKEN = 'bdbdfb49786b44b7bc4e0eddd4dba9ae'
PYOWM_CLIENT_TOKEN = 'ba58abbdec163813716f64cf4138d36b'

DEBUG = False

def main():

    ai = apiai.ApiAI(APIAI_CLIENT_TOKEN)

    print ("======================================================")
    print ("========= G I Z M O   T E S T   C L I E N T ==========")
    print ("======================================================")
    print ()
    print ("Type questions for Gizmo, type \'exit\' when done")

    while True:

        print(u"> ", end=u"")
        user_message = input()

        if user_message == '':
            print ("> I didn't catch that? Can you try again?")
            continue

        if user_message == u"exit":
            break

        request = ai.text_request()
        request.session_id = str(uuid.uuid4)

        request.query = user_message

        response = json.loads(request.getresponse().read().decode())

        if DEBUG:
            print ("DEBUG " + json.dumps(response))

        reply = response['result']['fulfillment']['speech']

        if reply.startswith("WEATHER"):

            data = reply.split(",")
            
            if data[1] == "NULL":
                location = "Kilcullen, Kildare, Ireland"
            else:
                location = data[1]

            owm = pyowm.OWM(PYOWM_CLIENT_TOKEN)
            obs = owm.weather_at_place(location)
            wet = obs.get_weather()
    
            reply = "Open Weather Map says "
            reply += wet.get_detailed_status() + ", "
            reply += "high of " + str(wet.get_temperature()['temp_max'] - 273.15) + "C, "
            reply += "low of " + str(wet.get_temperature()['temp_min'] - 273.15) + "C, "
            reply += "wind " + str(wet.get_wind()['speed']) + "km/h, "
            reply += "heading " + str(wet.get_wind()['deg']) + "deg."

            if DEBUG:
                loc = obs.get_location()
                reply += "(" + loc.get_name() + " - " + str(loc.get_lat()) + "," + str(loc.get_lon()) +")"

        if reply.startswith("HEATING"):

            data = reply.split(",")

            if data[1] == "ON":
                if data[2] == "NULL":
                    reply = "OK, Turning heating on..."
                else:
                    reply = "OK, Boosting heating for " + data[2]+"..."
            else:
                reply = "OK, turning heating off..."

        ### Print the final reply

        print ("< " + reply)

if __name__ == '__main__':
	main()

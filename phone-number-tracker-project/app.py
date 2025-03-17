from flask import Flask, render_template, request
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
import mysql.connector
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="phone_tracker"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    data = {}
    if request.method == "POST":
        phone_number = request.form.get("number")

        try:
            parsed_number = phonenumbers.parse(phone_number)
            if phonenumbers.is_valid_number(parsed_number):
                data["number"] = phone_number
                data["time_zone"] = ", ".join(timezone.time_zones_for_number(parsed_number))
                data["carrier"] = carrier.name_for_number(parsed_number, 'en')
                data["region"] = geocoder.description_for_number(parsed_number, 'en')

                # Get Latitude & Longitude
                geolocator = Nominatim(user_agent="phone_tracker")
                location = geolocator.geocode(data["region"])
                if location:
                    data["latitude"] = location.latitude
                    data["longitude"] = location.longitude

                # Save to Database
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO user_details (Timezone, Region, Number) VALUES (%s, %s, %s)", 
                               (data["time_zone"], data["region"], phone_number))
                db.commit()
                cursor.close()
                db.close()

        except:
            data["error"] = "Invalid phone number!"

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)

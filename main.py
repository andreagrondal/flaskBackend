from flask import Flask, render_template, request, jsonify

import openai
import os
from flask_cors import CORS

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)
openai.api_key = 'YOUR API_KEY HERE!'


@app.route("/<dest>", methods=["GET", "POST"])
def home(dest):
    if request.method == "POST":

        trip_response = get_trip(dest)

        return jsonify(trip_response)

    return render_template("index.html")


def get_trip(regions, klima, interests, countries):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
              "role": "system",
              "content": "You are a travel guide who is an expert at planning where to go on vacation."
              "The user is gonna tell you some preferences and you are going to give them a place in a country they are going to. You have to tell them this is your surprise trip."
            },
            {
                "role": "user",
                "content": f"What do you want to do?: {regions, klima, interests, countries}"
            }
        ],
        temperature=0.8,
        max_tokens=800,

    )

    content_list = response.choices[0].message.content

    return content_list


def get_daytrip(destination):
    print(1, destination)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
              "role": "system",
              "content": "You are a travel guide who is an expert at planning where to go on vacation."
              "The user is gonna tell you what they want to do that day, and you will give them a good and detailed plan for the day, with times and how to get there."
            },
            {
                "role": "user",
                "content": f"What do you want to do?: {destination}"
            }
        ],
        temperature=0.8,
        max_tokens=800,
    )

    content_list = response.choices[0].message.content

    print(2, content_list)
    return content_list


@app.route("/generateDay", methods=["GET", "POST"])
def day():
    data = request.get_json()

    trip_response = get_daytrip(data)

    return jsonify(trip_response)


@app.route("/generateTravelPlan", methods=["POST"])
def generate_travel_plan():
    data = request.get_json()
    # Hent preferanser fra data
    selectedRegions = data.get("selectedRegions", [])
    selectedKlima = data.get("selectedKlima", [])
    selectedInterest = data.get("selectedInterest", [])
    selectedCountries = data.get("selectedCountries", [])

    # Gjør behandling her, som for eksempel å spørre OpenAI API
    # Eksempel bruker kun det første landet. Tilpass etter behov.
    trip_response = get_trip(
        selectedRegions[0:] if selectedRegions else "whatever",
        selectedKlima[0:] if selectedKlima else "whatever",
        selectedInterest[0:] if selectedInterest else "whatever",
        selectedCountries[0:] if selectedCountries else "whatever",
    )

    return jsonify({"message": trip_response})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4040)

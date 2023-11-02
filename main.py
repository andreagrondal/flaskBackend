from flask import Flask, redirect, render_template, request, url_for, jsonify
# from flask_bootstrap import Bootstrap5
import openai
import os
from flask_cors import CORS

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)
# app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
openai.api_key = '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'
# bootstrap = Bootstrap5(app)


@app.route("/<dest>", methods=["GET", "POST"])
def home(dest):
    if request.method == "POST":
        print(dest)

        trip_response = get_trip(dest)
        print(trip_response)

        return jsonify(trip_response)

    return render_template("index.html")


def get_trip(regions, klima, interests, countries):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
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

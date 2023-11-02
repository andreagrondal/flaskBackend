from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = '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'

@app.route('/generateTravelPlan', methods=['POST', 'GET'])
def generate_travel_plan():
    data = request.json

    # Get preferences from the POST data
    selectedRegions = data.get('selectedRegions', [])
    selectedKlima = data.get('selectedKlima', [])
    selectedInterest = data.get('selectedInterest', [])
    selectedCountries = data.get('selectedCountries', [])
    
    # TODO: Interface with ChatGPT API using the above preferences and generate a message.
    # For now, we'll return a sample message.
    message = "Thank you for selecting your preferences. Here's your travel plan based on your choices."

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4040)

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pickle
from datetime import datetime

app = Flask(__name__)
CORS(app)

model = pickle.load(open('model.pkl', 'rb'))

airline_dict = {'AirAsia': 0, "Indigo": 1, "GO_FIRST": 2, "SpiceJet": 3, "Air_India": 4, "Vistara": 5}
source_dict = {'Delhi': 0, "Hyderabad": 1, "Bangalore": 2, "Mumbai": 3, "Kolkata": 4, "Chennai": 5}
destination_dict = source_dict
departure_dict = arrival_dict = {'Early_Morning': 0, "Morning": 1, "Afternoon": 2, "Evening": 3, "Night": 4, "Late_Night": 5}
stops_dict = {'zero': 0, "one": 1, "two_or_more": 2}
class_dict = {'Economy': 0, 'Business': 1}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    try:
        features = [
            airline_dict[data['airline']],
            source_dict[data['source_city']],
            departure_dict[data['departure_time']],
            stops_dict[data['stops']],
            arrival_dict[data['arrival_time']],
            destination_dict[data['destination_city']],
            class_dict[data['class']],
            (datetime.strptime(data['departure_date'], '%Y-%m-%d') - datetime.today()).days + 1
        ]
        prediction = model.predict([features])[0]
        return render_template("result.html", prediction=round(prediction, 2))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

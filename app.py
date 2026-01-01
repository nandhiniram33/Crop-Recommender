from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')


# Crop Recommendation
@app.route('/recommend_crop', methods=['POST'])
def recommend_crop():
    soil = request.form['soil']
    season = request.form['season']
    temp = int(request.form['temperature'])

    if soil == "Clay" and season == "Rainy":
        crop = "Rice"
    elif soil == "Sandy" and season == "Summer":
        crop = "Groundnut"
    else:
        crop = "Maize"

    return jsonify({"crop": crop})


# Disease Detection (Demo)
@app.route('/detect_disease', methods=['POST'])
def detect_disease():
    # Static demo output
    return jsonify({"disease": "Leaf Blight"})


# Weather-Based Suggestion
@app.route('/weather_crop', methods=['POST'])
def weather_crop():
    rainfall = int(request.form['rainfall'])

    if rainfall > 200:
        crop = "Rice"
    elif rainfall > 100:
        crop = "Millet"
    else:
        crop = "Wheat"

    return jsonify({"crop": crop})


# Market Price Prediction
@app.route('/predict_price', methods=['POST'])
def predict_price():
    crop = request.form['crop']

    prices = {
        "Rice": "₹2200/quintal",
        "Wheat": "₹2100/quintal",
        "Maize": "₹1800/quintal"
    }

    price = prices.get(crop, "Price not available")
    return jsonify({"price": price})


# Voice-Based Info
@app.route('/crop_info', methods=['POST'])
def crop_info():
    info = "Rice grows well in clay soil with high rainfall and warm climate."
    return jsonify({"info": info})


if __name__ == '__main__':
    app.run(debug=True)

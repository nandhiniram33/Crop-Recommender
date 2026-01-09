
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import sys
import logging

try:
    from google.cloud import vision
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("WARNING: google-cloud-vision not installed. Install with: pip install google-cloud-vision")

import io

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Fertilizer Recommendation
@app.route('/recommend_fertilizer', methods=['POST'])
def recommend_fertilizer():
    crop = request.form.get('crop', '').strip().lower()
    lang = request.form.get('lang', 'en')
    crop_map_ta = {
        "அரிசி": "rice",
        "கோதுமை": "wheat",
        "மக்காசோளம்": "maize",
        "நிலக்கடலை": "groundnut",
        "சோளம்": "sorghum",
    "கம்பு": "pearl_millet",
    "ராகி": "finger_millet",
    "பருத்தி": "cotton",
    "கரும்பு": "sugarcane",
    "பருப்பு": "pulses",
    "சோயாபீன்": "soybean",
    "பயறு": "black_gram",
    "உளுந்து": "green_gram",
    "வாழை": "banana",
    "தேங்காய்": "coconut"
    }
    crop_key = crop_map_ta.get(crop, crop)
    fert_en = {
        "rice": "Urea, DAP, Potash",
        "wheat": "Urea, SSP, MOP",
        "maize": "Urea, DAP",
        "groundnut": "Gypsum, SSP",
         "sorghum": "Urea, DAP",
    "pearl_millet": "Urea, SSP",
    "finger_millet": "Urea, DAP",
    "cotton": "Urea, DAP, Potash",
    "sugarcane": "Urea, DAP, MOP",
    "pulses": "DAP, SSP",
    "soybean": "DAP, SSP",
    "black_gram": "DAP, SSP",
    "green_gram": "DAP, SSP",
    "banana": "Urea, Potash",
    "coconut": "Urea, MOP, Organic manure"
    }
    fert_ta = {
        "rice": "யூரியா, டிஏபி, பொட்டாஷ்",
        "wheat": "யூரியா, எஸ்எஸ்பி, எம்ஓபி",
        "maize": "யூரியா, டிஏபி",
        "groundnut": "ஜிப்சம், எஸ்எஸ்பி",
        "sorghum": "யூரியா, டிஏபி",
    "pearl_millet": "யூரியா, எஸ்எஸ்பி",
    "finger_millet": "யூரியா, டிஏபி",
    "cotton": "யூரியா, டிஏபி, பொட்டாஷ்",
    "sugarcane": "யூரியா, டிஏபி, எம்ஓபி",
    "pulses": "டிஏபி, எஸ்எஸ்பி",
    "soybean": "டிஏபி, எஸ்எஸ்பி",
    "black_gram": "டிஏபி, எஸ்எஸ்பி",
    "green_gram": "டிஏபி, எஸ்எஸ்பி",
    "banana": "யூரியா, பொட்டாஷ்",
    "coconut": "யூரியா, எம்ஓபி, இயற்கை உரம்"
    }
    if lang == 'ta':
        fert = fert_ta.get(crop_key, f"{crop}க்கு உரம் தகவல் இல்லை.")
    else:
        fert = fert_en.get(crop_key, f"No fertilizer data for {crop if crop else 'this crop'}")
    return jsonify({"fertilizer": fert})

# Crop Calendar
@app.route('/crop_calendar', methods=['POST'])
def crop_calendar():
    crop = request.form.get('crop', '').strip().lower()
    lang = request.form.get('lang', 'en')
    crop_map_ta = {
        "அரிசி": "rice",
        "கோதுமை": "wheat",
        "மக்காசோளம்": "maize",
        "நிலக்கடலை": "groundnut",
         "சோளம்": "sorghum",
    "கம்பு": "pearl_millet",
    "ராகி": "finger_millet",
    "பருத்தி": "cotton",
    "கரும்பு": "sugarcane",
    "சோயாபீன்": "soybean",
    "உளுந்து": "black_gram",
    "பயறு": "green_gram",
    "வாழை": "banana",
    "தேங்காய்": "coconut"
    }
    crop_key = crop_map_ta.get(crop, crop)
    cal_en = {
        "rice": "Sowing: June-July, Harvest: Nov-Dec",
        "wheat": "Sowing: Nov-Dec, Harvest: Mar-Apr",
        "maize": "Sowing: May-June, Harvest: Sep-Oct",
        "groundnut": "Sowing: June, Harvest: Sep",
         "sorghum": "Sowing: June–July, Harvest: Oct–Nov",
    "pearl_millet": "Sowing: June–July, Harvest: Sep–Oct",
    "finger_millet": "Sowing: June–July, Harvest: Oct–Nov",
    "cotton": "Sowing: June–July, Harvest: Dec–Jan",
    "sugarcane": "Sowing: Feb–Mar, Harvest: Jan–Mar (next year)",
    "soybean": "Sowing: June–July, Harvest: Sep–Oct",
    "black_gram": "Sowing: July–Aug, Harvest: Oct–Nov",
    "green_gram": "Sowing: July–Aug, Harvest: Oct–Nov",
    "banana": "Planting: Year-round, Harvest: 10–12 months",
    "coconut": "Planting: June–July, Harvest: After 4–5 years"
    }
    cal_ta = {
        "rice": "விதைப்பு: ஜூன்-ஜூலை, அறுவடை: நவ-டிச",
        "wheat": "விதைப்பு: நவ-டிச, அறுவடை: மார்ச்-ஏப்",
        "maize": "விதைப்பு: மே-ஜூன், அறுவடை: செப்-அக்",
        "groundnut": "விதைப்பு: ஜூன், அறுவடை: செப்"
    }
    if lang == 'ta':
        cal = cal_ta.get(crop_key, f"{crop}க்கு காலண்டர் இல்லை.")
    else:
        cal = cal_en.get(crop_key, f"No calendar data for {crop if crop else 'this crop'}")
    return jsonify({"calendar": cal})

# Location-Based Crop Suggestion
@app.route('/location_crop', methods=['POST'])
def location_crop():
    lat = request.form.get('latitude', type=float)
    crop = "Rice"
    if lat is not None:
        crop = "Wheat" if lat > 20 else "Rice"
    return jsonify({"crop": crop})

# Crop Calendar

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
    lang = request.form.get('lang', 'en')
    if soil == "Clay" and season == "Rainy":
        crop = "Rice"
    elif soil == "Sandy" and season == "Summer":
        crop = "Groundnut"
    else:
        crop = "Maize"
    crop_ta = {
        "Rice": "அரிசி",
        "Groundnut": "நிலக்கடலை",
        "Maize": "மக்காசோளம்"
    }
    if lang == 'ta':
        crop = crop_ta.get(crop, crop)
    return jsonify({"crop": crop})


# Disease Detection using Google Cloud Vision API
@app.route('/detect_disease', methods=['POST'])
def detect_disease():
    try:
        logger.info("=== DISEASE DETECTION STARTED ===")
        
        # Accept image upload
        if 'image' not in request.files:
            return jsonify({
                "error": "No image uploaded",
                "disease": "Unknown",
                "confidence": 0,
                "status": "error"
            })
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({
                "error": "No file selected",
                "disease": "Unknown",
                "confidence": 0,
                "status": "error"
            })
        
        filename = secure_filename(image_file.filename)
        logger.info(f"Processing image: {filename}")
        
        # Read image content
        content = image_file.read()
        if not content:
            return jsonify({
                "error": "Empty image file",
                "disease": "Unknown",
                "confidence": 0,
                "status": "error"
            })

        logger.info(f"Image size: {len(content)} bytes")

        # Check if google-cloud-vision is available FIRST
        if not VISION_AVAILABLE:
            logger.error("Google Cloud Vision library is NOT available!")
            return jsonify({
                "error": "Google Cloud Vision library not installed",
                "disease": "Library Missing",
                "confidence": 0,
                "status": "error"
            })
        
        logger.info("✓ Google Cloud Vision library available")

        # Set environment variable for credentials
        cred_path = os.path.join(os.path.dirname(__file__), 'vision-key.json')
        logger.info(f"Credentials path: {cred_path}")
        logger.info(f"Credentials exist: {os.path.exists(cred_path)}")
        
        if not os.path.exists(cred_path):
            logger.error(f"Credentials file NOT found at: {cred_path}")
            return jsonify({
                "error": f"vision-key.json not found",
                "disease": "Credentials Missing",
                "confidence": 0,
                "status": "error"
            })
        
        logger.info("✓ Credentials file found")

        # Set environment variable
       # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"c:\Users\hp\Downloads\Project1nandyrecomended\Project1nandy\Project1\vision-key.json"
        logger.info("✓ Environment variable set")

        # Initialize the Vision API client
        logger.info("Initializing Vision API client...")
        try:
            client = vision.ImageAnnotatorClient.from_service_account_file(r"C:\Users\hp\Downloads\Project1nandyrecomended\Project1nandy\Project1\vision-key.json")
            logger.info("✓ Vision API client initialized successfully")
        except Exception as client_error:
            logger.error(f"Failed to initialize client: {str(client_error)}")
            return jsonify({
                "error": f"Failed to initialize Vision API: {str(client_error)}",
                "disease": "API Error",
                "confidence": 0,
                "status": "error"
            })
        
        image = vision.Image(content=content)
        logger.info("✓ Image object created")
        
        # Perform label detection
        logger.info("Performing label detection on image...")
        try:
            response = client.label_detection(image=image)
            labels = response.label_annotations
            logger.info(f"✓ API call successful. Received {len(labels)} labels")
        except Exception as api_error:
            error_str = str(api_error)
            logger.error(f"API call failed with error: {error_str}")
            logger.error(f"Error type: {type(api_error).__name__}")
            import traceback
            logger.error(f"Full traceback:\n{traceback.format_exc()}")
            
            # Check if it's a billing error - Use demo mode
            if "BILLING_DISABLED" in error_str or "billing" in error_str.lower():
                logger.warning("BILLING DISABLED - Using Demo Mode with AI Simulation")
                
                # Demo detection based on filename
                demo_diseases = {
                    "leaf blight": {
                        "disease": "Leaf Blight Disease",
                        "confidence": 85.3,
                        "labels": [
                            {"name": "Leaf", "score": 94.2},
                            {"name": "Blight", "score": 88.5},
                            {"name": "Plant Disease", "score": 85.3},
                            {"name": "Brown Spots", "score": 82.1},
                            {"name": "Infected Leaf", "score": 79.7}
                        ]
                    }
                }
                
                # Check filename for hints
                filename_lower = filename.lower()
                for key, demo_result in demo_diseases.items():
                    if key in filename_lower:
                        logger.info(f"Using demo result for: {key}")
                        return jsonify({
                            "disease": demo_result["disease"],
                            "confidence": demo_result["confidence"],
                            "labels": demo_result["labels"],
                            "status": "demo",
                            "message": "Using Demo Mode (Billing Disabled on Google Cloud Project)"
                        })
                
                # Generic demo response
                return jsonify({
                    "disease": "Leaf Spot Disease (Demo)",
                    "confidence": 82.5,
                    "labels": [
                        {"name": "Leaf", "score": 93.2},
                        {"name": "Plant", "score": 87.4},
                        {"name": "Spots", "score": 82.5},
                        {"name": "Disease", "score": 78.1},
                        {"name": "Damaged Plant", "score": 75.6}
                    ],
                    "status": "demo",
                    "message": "Demo Mode: Google Cloud Vision API billing disabled."
                })
            
            return jsonify({
                "error": f"Vision API Error: {error_str}",
                "disease": "API Failed",
                "confidence": 0,
                "status": "error",
                "error_type": type(api_error).__name__
            })
        
        # Disease keywords to look for in labels
        disease_keywords = {
            "leaf": "Leaf Disease",
            "rust": "Rust Disease",
            "spot": "Leaf Spot Disease",
            "mold": "Mold/Fungal Disease",
            "blight": "Blight Disease",
            "rot": "Rot Disease",
            "wilt": "Wilt Disease",
            "canker": "Canker Disease",
            "scab": "Scab Disease",
            "powdery": "Powdery Mildew",
            "yellow": "Yellow Mosaic Virus",
            "mosaic": "Mosaic Virus",
            "necrosis": "Necrosis",
            "damage": "Plant Damage",
            "insect": "Insect Damage",
            "pest": "Pest Infestation",
            "infected": "Infected Plant",
            "diseased": "Diseased Plant",
            "brown": "Brown Spot Disease",
            "black": "Black Spot Disease"
        }
        
        detected_disease = "No Disease Detected"
        confidence = 0.0
        matched_labels = []
        
        # Analyze labels to find disease indicators
        if labels:
            logger.info(f"Analyzing {len(labels)} labels for disease indicators...")
            
            for idx, label in enumerate(labels[:20]):  # Check top 20 labels
                label_desc = label.description.lower()
                label_score = label.score
                
                matched_labels.append({
                    "name": label.description,
                    "score": round(label_score * 100, 2)
                })
                
                logger.debug(f"Label {idx+1}: '{label.description}' (Score: {label_score*100:.1f}%)")
                
                # Check each label against disease keywords
                for keyword, disease_name in disease_keywords.items():
                    if keyword in label_desc:
                        detected_disease = disease_name
                        confidence = round(label_score * 100, 2)
                        logger.info(f"✓ Disease detected: {disease_name} (Confidence: {confidence}%)")
                        break
                
                # If we found a disease with good confidence, break
                if detected_disease != "No Disease Detected" and confidence > 25:
                    logger.info(f"High confidence disease found, stopping search")
                    break
        else:
            logger.warning("No labels received from Vision API")
        
        logger.info(f"Final result: {detected_disease} ({confidence}%)")
        logger.info("=== DISEASE DETECTION COMPLETED ===")
        
        return jsonify({
            "disease": detected_disease,
            "confidence": confidence,
            "labels": matched_labels[:5],
            "status": "success"
        })
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"EXCEPTION in detect_disease: {error_msg}")
        import traceback
        logger.error(traceback.format_exc())
        
        return jsonify({
            "error": error_msg,
            "disease": "Error in analysis",
            "confidence": 0,
            "status": "error"
        })


# Weather-Based Suggestion
@app.route('/weather_crop', methods=['POST'])
def weather_crop():
    rainfall = int(request.form['rainfall'])
    lang = request.form.get('lang', 'en')
    if rainfall > 200:
        crop = "Rice"
    elif rainfall > 100:
        crop = "Millet"
    else:
        crop = "Wheat"
    crop_ta = {
        "Rice": "அரிசி",
        "Millet": "கம்பு",
        "Wheat": "கோதுமை"
    }
    if lang == 'ta':
        crop = crop_ta.get(crop, crop)
    return jsonify({"crop": crop})


# Market Price Prediction
@app.route('/predict_price', methods=['POST'])
def predict_price():
    crop = request.form['crop'].strip().capitalize()

    prices = {
        "Rice": "₹2200/quintal",
        "Wheat": "₹2100/quintal",
        "Maize": "₹1800/quintal",
        "Groundnut": "₹4000/quintal",
        "Millet": "₹1500/quintal",
        "Soybean": "₹3500/quintal",
        "Millet": "₹2500/quintal",
    "Soybean": "₹4600/quintal",
    "Sorghum": "₹2970/quintal",
    "Pearl Millet": "₹2500/quintal",
    "Finger Millet": "₹3846/quintal",
    "Cotton": "₹6620/quintal",
    "Sugarcane": "₹340/quintal",
    "Black Gram": "₹6600/quintal",
    "Green Gram": "₹8558/quintal",
    "Chickpea": "₹5440/quintal",
    "Pigeon Pea": "₹7550/quintal",
    "Mustard": "₹5650/quintal",
    "Sunflower": "₹6760/quintal",
    "Barley": "₹1850/quintal"
    }

    price = prices.get(crop, f"No price data for {crop}")
    return jsonify({"price": price})



# Voice-Based Info with Tamil support
@app.route('/crop_info', methods=['POST'])
def crop_info():
    crop = request.form.get('crop', '').strip().capitalize()
    lang = request.form.get('lang', 'en')
    crop_infos_en = {
        "Rice": "Rice grows well in clay soil with high rainfall and warm climate.",
        "Wheat": "Wheat prefers well-drained loamy soil and cooler climates.",
        "Maize": "Maize thrives in warm weather and well-drained fertile soil.",
        "Groundnut": "Groundnut grows best in sandy soil during summer.",
        "Millet": "Millet is suitable for dry regions and moderate rainfall.",
        "Soybean": "Soybean prefers loamy soil and moderate rainfall.",
        "Sorghum": "Sorghum grows well in dry regions with low rainfall.",
    "Pearl Millet": "Pearl millet is drought-resistant and grows in sandy soil.",
    "Finger Millet": "Finger millet prefers red soil and moderate rainfall.",
    "Cotton": "Cotton requires black soil and a warm climate with moderate rainfall.",
    "Sugarcane": "Sugarcane needs fertile soil, high rainfall, and long warm periods.",
    "Banana": "Banana grows well in rich loamy soil with plenty of water.",
    "Coconut": "Coconut prefers sandy loam soil and coastal climate.",
    "Black Gram": "Black gram grows well in loamy soil with low to moderate rainfall.",
    "Green Gram": "Green gram prefers well-drained soil and warm climate.",
    "Chickpea": "Chickpea grows best in dry climates with well-drained soil."
    }
    crop_infos_ta = {
        "Rice": "அரிசி களிமண் மற்றும் அதிக மழை, வெப்பமான காலநிலையில் நன்கு வளரும்.",
        "Wheat": "கோதுமை நன்கு வடிகாலமைந்த லோமி மண் மற்றும் குளிர்ந்த காலநிலையை விரும்புகிறது.",
        "Maize": "மக்காசோளம் வெப்பமான காலநிலையும், நன்கு வளமான மண்ணையும் விரும்புகிறது.",
        "Groundnut": "நிலக்கடலை கோடை பருவத்தில் மணல் மண்ணில் சிறப்பாக வளரும்.",
        "Millet": "கம்பு வறண்ட பகுதிகளுக்கும், மிதமான மழைக்கும் ஏற்றது.",
        "Soybean": "சோயாபீன் லோமி மண் மற்றும் மிதமான மழையை விரும்புகிறது.",
         "Sorghum": "சோளம் குறைந்த மழை உள்ள வறண்ட பகுதிகளில் நன்கு வளரும்.",
    "Pearl Millet": "கம்பு வறட்சியை தாங்கும் தன்மை கொண்டது மற்றும் மணல் மண்ணில் வளரும்.",
    "Finger Millet": "ராகி சிவப்பு மண் மற்றும் மிதமான மழையை விரும்புகிறது.",
    "Cotton": "பருத்தி கரிமண் மற்றும் வெப்பமான காலநிலையை விரும்புகிறது.",
    "Sugarcane": "கரும்பு வளமான மண், அதிக மழை மற்றும் நீண்ட வெப்ப காலத்தை தேவைப்படுத்துகிறது.",
    "Banana": "வாழை செழுமையான லோமி மண்ணிலும், அதிக நீர்ப்பாசனத்துடன் நன்கு வளரும்.",
    "Coconut": "தேங்காய் மணல் கலந்த லோமி மண் மற்றும் கடற்கரை காலநிலையை விரும்புகிறது.",
    "Black Gram": "உளுந்து லோமி மண் மற்றும் குறைந்த முதல் மிதமான மழையில் நன்கு வளரும்.",
    "Green Gram": "பயறு நன்கு வடிகாலமைந்த மண் மற்றும் வெப்பமான காலநிலையை விரும்புகிறது.",
    "Chickpea": "கொண்டைக்கடலை வறண்ட காலநிலை மற்றும் நன்கு வடிகாலமைந்த மண்ணில் நன்கு வளரும்."
    }
    # Accept Tamil crop names as well
    crop_map_ta = {
        "அரிசி": "Rice",
        "கோதுமை": "Wheat",
        "மக்காசோளம்": "Maize",
        "நிலக்கடலை": "Groundnut",
        "கம்பு": "Millet",
        "சோயாபீன்": "Soybean",
         "கம்பு": "pearl_millet",
    "ராகி": "finger_millet",
    "பருத்தி": "cotton",
    "கரும்பு": "sugarcane",
    "சோயாபீன்": "soybean",
    "உளுந்து": "black_gram",
    "பயறு": "green_gram",
    "வாழை": "banana",
    "தேங்காய்": "coconut"
    }
    crop_key = crop
    if lang == 'ta':
        # If input is Tamil, map to English key
        crop_key = crop_map_ta.get(crop, crop)
        info = crop_infos_ta.get(crop_key, f"{crop} பற்றிய தகவல் இல்லை.")
    else:
        # If input is Tamil, map to English key for English info
        crop_key = crop_map_ta.get(crop, crop)
        info = crop_infos_en.get(crop_key, f"No info available for {crop if crop else 'this crop'}.")
    return jsonify({"info": info})


if __name__ == '__main__':
    app.run(debug=True)

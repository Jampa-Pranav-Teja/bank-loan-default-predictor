from flask import Flask, request, jsonify
import os
from loan_model import LoanDefaultPredictor  # your model file

app = Flask(__name__)

# Initialize the model
predictor = LoanDefaultPredictor()

# Try to load existing model
try:
    predictor.load_model('loan_model.pkl')
    MODEL_LOADED = True
    print("Trained model loaded successfully!")
except:
    MODEL_LOADED = False
    print("No trained model found. Using mock prediction logic.")


# Root route
@app.route('/')
def home():
    return jsonify({
        'message': 'Loan Prediction API is running!',
        'routes': ['/predict (POST)', '/health (GET)']
    })


# Health route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': MODEL_LOADED
    })


# Predict route (POST)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        if MODEL_LOADED:
            result = predictor.predict(data)
        else:
            result = mock_prediction(data)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Predict route (GET) – browser-friendly
@app.route('/predict', methods=['GET'])
def predict_info():
    return jsonify({
        "message": "Send a POST request with JSON loan data to get prediction",
        "example": {
            "credit_score": 650,
            "dtir1": 40,
            "ltv": 85,
            "income": 50000,
            "loan_amount": 200000,
            "credit_worthiness": "Fair"
        }
    })


# Mock prediction logic
def mock_prediction(data):
    risk_score = 0
    risk_factors = []

    credit_score = int(data.get('credit_score', 0))
    if credit_score < 600:
        risk_score += 30
        risk_factors.append('Low Credit Score')
    elif credit_score < 700:
        risk_score += 15
        risk_factors.append('Fair Credit Score')

    dtir = float(data.get('dtir1', 0))
    if dtir > 43:
        risk_score += 25
        risk_factors.append('High Debt-to-Income Ratio')
    elif dtir > 36:
        risk_score += 10
        risk_factors.append('Moderate Debt-to-Income Ratio')

    ltv = float(data.get('ltv', 0))
    if ltv > 90:
        risk_score += 20
        risk_factors.append('High Loan-to-Value Ratio')
    elif ltv > 80:
        risk_score += 10
        risk_factors.append('Moderate Loan-to-Value Ratio')

    income = int(data.get('income', 0))
    loan_amount = int(data.get('loan_amount', 0))
    if income > 0 and loan_amount > 0:
        income_ratio = loan_amount / income
        if income_ratio > 5:
            risk_score += 15
            risk_factors.append('High Loan-to-Income Ratio')

    credit_worthiness = data.get('credit_worthiness', '')
    if credit_worthiness == 'Poor':
        risk_score += 20
        risk_factors.append('Poor Credit Worthiness')
    elif credit_worthiness == 'Fair':
        risk_score += 10
        risk_factors.append('Fair Credit Worthiness')

    # Determine prediction
    if risk_score <= 20:
        prediction = 'approved'
        confidence = 85 + (15 * (20 - risk_score) / 20)
        recommendation = 'Low risk application. Recommended for approval with standard terms.'
    elif risk_score <= 50:
        prediction = 'review'
        confidence = 70 + (15 * (50 - risk_score) / 30)
        recommendation = 'Moderate risk application. Manual review recommended with possible adjusted terms.'
    else:
        prediction = 'rejected'
        confidence = 75 + (15 * min(risk_score - 50, 30) / 30)
        recommendation = 'High risk application. Consider rejection or require additional collateral/co-signer.'

    return {
        'prediction': prediction,
        'confidence': round(confidence, 1),
        'risk_factors': risk_factors if risk_factors else ['Standard Risk Profile'],
        'recommendation': recommendation
    }


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

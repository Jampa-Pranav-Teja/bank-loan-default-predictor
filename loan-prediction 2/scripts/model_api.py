from flask import Flask, request, jsonify
import pandas as pd
import sys
import os
from loan_model import LoanDefaultPredictor

app = Flask(__name__)

# Initialize the model
predictor = LoanDefaultPredictor()

# Try to load existing model, otherwise use the mock prediction logic
try:
    predictor.load_model('loan_model.pkl')
    MODEL_LOADED = True
    print("Trained model loaded successfully!")
except:
    MODEL_LOADED = False
    print("No trained model found. Using mock prediction logic.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        if MODEL_LOADED:
            # Use the trained model
            result = predictor.predict(data)
        else:
            # Use mock prediction logic (same as in the Next.js API)
            result = mock_prediction(data)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def mock_prediction(data):
    """Mock prediction logic when no trained model is available"""
    risk_score = 0
    risk_factors = []
    
    # Credit Score Analysis
    credit_score = int(data.get('credit_score', 0)) if data.get('credit_score') else 0
    if credit_score < 600:
        risk_score += 30
        risk_factors.append('Low Credit Score')
    elif credit_score < 700:
        risk_score += 15
        risk_factors.append('Fair Credit Score')
    
    # Debt-to-Income Ratio
    dtir = float(data.get('dtir1', 0)) if data.get('dtir1') else 0
    if dtir > 43:
        risk_score += 25
        risk_factors.append('High Debt-to-Income Ratio')
    elif dtir > 36:
        risk_score += 10
        risk_factors.append('Moderate Debt-to-Income Ratio')
    
    # Loan-to-Value Ratio
    ltv = float(data.get('ltv', 0)) if data.get('ltv') else 0
    if ltv > 90:
        risk_score += 20
        risk_factors.append('High Loan-to-Value Ratio')
    elif ltv > 80:
        risk_score += 10
        risk_factors.append('Moderate Loan-to-Value Ratio')
    
    # Income Analysis
    income = int(data.get('income', 0)) if data.get('income') else 0
    loan_amount = int(data.get('loan_amount', 0)) if data.get('loan_amount') else 0
    if income > 0 and loan_amount > 0:
        income_ratio = loan_amount / income
        if income_ratio > 5:
            risk_score += 15
            risk_factors.append('High Loan-to-Income Ratio')
    
    # Credit Worthiness
    if data.get('credit_worthiness') == 'Poor':
        risk_score += 20
        risk_factors.append('Poor Credit Worthiness')
    elif data.get('credit_worthiness') == 'Fair':
        risk_score += 10
        risk_factors.append('Fair Credit Worthiness')
    
    # Determine prediction based on risk score
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

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': MODEL_LOADED
    })

@app.route('/')
def home():
    return jsonify({
        'message': 'Loan Prediction API is running!',
        'routes': ['/predict (POST)', '/health (GET)']
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

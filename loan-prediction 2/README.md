# Bank Loan Default Prediction System

A comprehensive web application for predicting loan default risk using machine learning. The system features a professional frontend interface built with Next.js and a Python-based ML model for accurate risk assessment.

## Features

- **Professional Web Interface**: Clean, trustworthy design inspired by financial platforms
- **Comprehensive Risk Assessment**: Analyzes 18 key factors including credit score, income, debt ratios, and property details
- **Real-time Predictions**: Instant risk assessment with confidence scores and recommendations
- **Machine Learning Backend**: Random Forest classifier with feature importance analysis
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Architecture

### Frontend (Next.js)
- Modern React-based interface with TypeScript
- Professional banking-inspired design using Tailwind CSS
- Real-time form validation and user feedback
- Responsive layout optimized for all devices

### Backend (Python)
- Scikit-learn Random Forest classifier
- Comprehensive data preprocessing pipeline
- Feature importance analysis
- Model persistence and loading capabilities

### API Integration
- Next.js API routes for seamless frontend-backend communication
- Flask API option for standalone Python service
- Mock prediction logic for demonstration purposes

## Getting Started

### Prerequisites
- Node.js 18+ for the frontend
- Python 3.8+ for the ML model
- Required Python packages (see requirements.txt)

### Installation

1. **Install Python dependencies:**
   \`\`\`bash
   pip install -r scripts/requirements.txt
   \`\`\`

2. **Train the model (optional):**
   \`\`\`bash
   # Using sample data
   python scripts/train_model.py
   
   # Using your own dataset
   python scripts/train_model.py path/to/your/dataset.csv
   \`\`\`

3. **Run the application:**
   The Next.js application includes everything needed to run the prediction system.

## Dataset Requirements

Your dataset should include the following columns:

### Required Features:
- `Gender`: Male, Female, Other
- `loan_type`: Personal, Home, Auto, Business
- `loan_purpose`: Home Purchase, Refinance, Cash Out, Other
- `Credit_Worthiness`: Excellent, Good, Fair, Poor
- `loan_amount`: Loan amount in dollars
- `term`: Loan term in months
- `property_value`: Property value in dollars
- `occupancy_type`: Owner Occupied, Investment, Second Home
- `Secured_by`: Real Estate, Vehicle, Other, Unsecured
- `total_units`: Number of units in property
- `income`: Annual income in dollars
- `credit_type`: EQUI, EXPR, CRF
- `Credit_Score`: Credit score (300-850)
- `co-applicant_credit_type`: EQUI, EXPR, CRF, None
- `age`: Applicant age
- `LTV`: Loan-to-Value ratio percentage
- `Region`: North, South, East, West, Central
- `dtir1`: Debt-to-Income ratio percentage

### Target Variable:
- `Status`: 0 for approved/no default, 1 for default

## Model Performance

The Random Forest model analyzes multiple risk factors:

### Key Risk Indicators:
- **Credit Score**: Primary factor in default prediction
- **Debt-to-Income Ratio**: Critical for assessing repayment capacity
- **Loan-to-Value Ratio**: Important for secured loans
- **Credit Worthiness**: Overall creditworthiness assessment
- **Income vs Loan Amount**: Affordability analysis

### Risk Assessment Logic:
- **Low Risk (Approved)**: Strong credit profile, low DTI, reasonable LTV
- **Moderate Risk (Review)**: Mixed indicators requiring manual review
- **High Risk (Rejected)**: Multiple negative factors present

## API Endpoints

### POST /api/predict
Predicts loan default risk based on application data.

**Request Body:**
\`\`\`json
{
  "gender": "Male",
  "loan_type": "Home",
  "loan_purpose": "Home Purchase",
  "credit_worthiness": "Good",
  "loan_amount": "250000",
  "term": "360",
  "property_value": "300000",
  "occupancy_type": "Owner Occupied",
  "secured_by": "Real Estate",
  "total_units": "1",
  "income": "75000",
  "credit_type": "EQUI",
  "credit_score": "720",
  "co_applicant_credit_type": "None",
  "age": "35",
  "ltv": "83.33",
  "region": "North",
  "dtir1": "28.5"
}
\`\`\`

**Response:**
\`\`\`json
{
  "prediction": "approved",
  "confidence": 87.5,
  "risk_factors": ["Standard Risk Profile"],
  "recommendation": "Low risk application. Recommended for approval with standard terms."
}
\`\`\`

## Customization

### Adding New Features
1. Update the `feature_columns` list in `loan_model.py`
2. Modify the preprocessing pipeline to handle new features
3. Update the frontend form to collect additional data
4. Retrain the model with the expanded feature set

### Adjusting Risk Thresholds
Modify the risk scoring logic in both the Python model and the mock prediction function to adjust sensitivity to different risk factors.

### Styling Customization
The application uses a professional color scheme defined in `globals.css`. Modify the CSS custom properties to match your brand colors while maintaining accessibility standards.

## Security Considerations

- Input validation on both frontend and backend
- Sanitization of user inputs
- Rate limiting for API endpoints (recommended for production)
- Secure model file storage
- HTTPS enforcement for production deployment

## Deployment

### Vercel (Recommended)
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy with automatic builds

### Docker Deployment
\`\`\`dockerfile
# Example Dockerfile for Python API
FROM python:3.9-slim
WORKDIR /app
COPY scripts/requirements.txt .
RUN pip install -r requirements.txt
COPY scripts/ .
CMD ["python", "model_api.py"]
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or issues:
1. Check the documentation
2. Review existing issues on GitHub
3. Create a new issue with detailed information

## Disclaimer

This tool provides risk assessment guidance and should be used alongside human judgment for final lending decisions. Always comply with applicable lending regulations and fair lending practices.

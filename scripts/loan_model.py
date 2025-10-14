import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import json

class LoanDefaultPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = [
            'Gender', 'loan_type', 'loan_purpose', 'Credit_Worthiness',
            'loan_amount', 'term', 'property_value', 'occupancy_type',
            'Secured_by', 'total_units', 'income', 'credit_type',
            'Credit_Score', 'co-applicant_credit_type', 'age', 'LTV',
            'Region', 'dtir1'
        ]
        
    def preprocess_data(self, df, is_training=True):
        """Preprocess the data for training or prediction"""
        df_processed = df.copy()
        
        # Handle categorical variables
        categorical_columns = [
            'Gender', 'loan_type', 'loan_purpose', 'Credit_Worthiness',
            'occupancy_type', 'Secured_by', 'credit_type', 
            'co-applicant_credit_type', 'Region'
        ]
        
        for col in categorical_columns:
            if col in df_processed.columns:
                if is_training:
                    # Fit and transform during training
                    le = LabelEncoder()
                    df_processed[col] = le.fit_transform(df_processed[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    # Transform using existing encoder during prediction
                    if col in self.label_encoders:
                        # Handle unseen categories
                        le = self.label_encoders[col]
                        df_processed[col] = df_processed[col].astype(str)
                        mask = df_processed[col].isin(le.classes_)
                        df_processed.loc[~mask, col] = le.classes_[0]  # Default to first class
                        df_processed[col] = le.transform(df_processed[col])
        
        # Handle numerical columns
        numerical_columns = [
            'loan_amount', 'term', 'property_value', 'total_units',
            'income', 'Credit_Score', 'age', 'LTV', 'dtir1'
        ]
        
        for col in numerical_columns:
            if col in df_processed.columns:
                df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
                df_processed[col] = df_processed[col].fillna(df_processed[col].median())
        
        return df_processed
    
    def train(self, df):
        """Train the model on the provided dataset"""
        print("Starting model training...")
        
        # Preprocess the data
        df_processed = self.preprocess_data(df, is_training=True)
        
        # Prepare features and target
        X = df_processed[self.feature_columns]
        y = df_processed['Status']  # Assuming 'Status' is the target column (0=approved, 1=default)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10))
        
        return accuracy
    
    def predict(self, data):
        """Make predictions on new data"""
        # Convert single record to DataFrame if needed
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = data.copy()
        
        # Preprocess the data
        df_processed = self.preprocess_data(df, is_training=False)
        
        # Ensure all required columns are present
        for col in self.feature_columns:
            if col not in df_processed.columns:
                df_processed[col] = 0  # Default value for missing columns
        
        # Select and order features
        X = df_processed[self.feature_columns]
        
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        # Get feature importance for this prediction
        feature_importance = dict(zip(self.feature_columns, self.model.feature_importances_))
        
        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            confidence = max(prob) * 100
            risk_factors = self._identify_risk_factors(df_processed.iloc[i], feature_importance)
            
            result = {
                'prediction': 'rejected' if pred == 1 else 'approved',
                'confidence': confidence,
                'risk_factors': risk_factors,
                'recommendation': self._generate_recommendation(pred, confidence, risk_factors)
            }
            results.append(result)
        
        return results[0] if len(results) == 1 else results
    
    def _identify_risk_factors(self, record, feature_importance):
        """Identify key risk factors for a specific record"""
        risk_factors = []
        
        # Check credit score
        if record.get('Credit_Score', 0) < 600:
            risk_factors.append('Low Credit Score')
        
        # Check debt-to-income ratio
        if record.get('dtir1', 0) > 43:
            risk_factors.append('High Debt-to-Income Ratio')
        
        # Check loan-to-value ratio
        if record.get('LTV', 0) > 90:
            risk_factors.append('High Loan-to-Value Ratio')
        
        # Check income vs loan amount
        income = record.get('income', 1)
        loan_amount = record.get('loan_amount', 0)
        if income > 0 and (loan_amount / income) > 5:
            risk_factors.append('High Loan-to-Income Ratio')
        
        return risk_factors if risk_factors else ['Standard Risk Profile']
    
    def _generate_recommendation(self, prediction, confidence, risk_factors):
        """Generate a recommendation based on prediction results"""
        if prediction == 0:  # Approved
            if confidence > 90:
                return "Low risk application. Recommended for approval with standard terms."
            else:
                return "Moderate-low risk application. Approved with standard monitoring."
        else:  # Rejected
            if len(risk_factors) > 3:
                return "High risk application. Recommend rejection or require significant additional collateral."
            else:
                return "Moderate-high risk application. Consider rejection or adjusted terms with co-signer."
    
    def save_model(self, filepath='loan_model.pkl'):
        """Save the trained model and preprocessors"""
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='loan_model.pkl'):
        """Load a trained model and preprocessors"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        print(f"Model loaded from {filepath}")

# Example usage and training script
if __name__ == "__main__":
    # Initialize the predictor
    predictor = LoanDefaultPredictor()
    
    # Load your dataset here
    # df = pd.read_csv('your_loan_dataset.csv')
    
    # For demonstration, create a sample dataset structure
    print("Loan Default Prediction Model")
    print("=" * 50)
    print("Required dataset columns:")
    for col in predictor.feature_columns:
        print(f"- {col}")
    print("- Status (target variable: 0=approved, 1=default)")
    print("\nTo use this model:")
    print("1. Load your dataset with the required columns")
    print("2. Call predictor.train(df) to train the model")
    print("3. Call predictor.save_model() to save the trained model")
    print("4. Use predictor.predict(data) for new predictions")
    
    # Example prediction format
    sample_data = {
        'Gender': 'Male',
        'loan_type': 'Home',
        'loan_purpose': 'Home Purchase',
        'Credit_Worthiness': 'Good',
        'loan_amount': 250000,
        'term': 360,
        'property_value': 300000,
        'occupancy_type': 'Owner Occupied',
        'Secured_by': 'Real Estate',
        'total_units': 1,
        'income': 75000,
        'credit_type': 'EQUI',
        'Credit_Score': 720,
        'co-applicant_credit_type': 'None',
        'age': 35,
        'LTV': 83.33,
        'Region': 'North',
        'dtir1': 28.5
    }
    
    print(f"\nSample prediction data format:")
    print(json.dumps(sample_data, indent=2))

import pandas as pd
import numpy as np
from loan_model import LoanDefaultPredictor
import os

def create_sample_dataset():
    """Create a sample dataset for demonstration purposes"""
    np.random.seed(42)
    n_samples = 1000
    
    # Generate sample data
    data = {
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'loan_type': np.random.choice(['Personal', 'Home', 'Auto', 'Business'], n_samples),
        'loan_purpose': np.random.choice(['Home Purchase', 'Refinance', 'Cash Out', 'Other'], n_samples),
        'Credit_Worthiness': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor'], n_samples, p=[0.2, 0.4, 0.3, 0.1]),
        'loan_amount': np.random.normal(200000, 100000, n_samples).clip(10000, 1000000),
        'term': np.random.choice([180, 240, 300, 360], n_samples),
        'property_value': np.random.normal(250000, 120000, n_samples).clip(50000, 1500000),
        'occupancy_type': np.random.choice(['Owner Occupied', 'Investment', 'Second Home'], n_samples, p=[0.7, 0.2, 0.1]),
        'Secured_by': np.random.choice(['Real Estate', 'Vehicle', 'Other', 'Unsecured'], n_samples, p=[0.6, 0.2, 0.1, 0.1]),
        'total_units': np.random.choice([1, 2, 3, 4], n_samples, p=[0.8, 0.15, 0.04, 0.01]),
        'income': np.random.normal(75000, 30000, n_samples).clip(20000, 300000),
        'credit_type': np.random.choice(['EQUI', 'EXPR', 'CRF'], n_samples),
        'Credit_Score': np.random.normal(700, 80, n_samples).clip(300, 850),
        'co-applicant_credit_type': np.random.choice(['EQUI', 'EXPR', 'CRF', 'None'], n_samples, p=[0.2, 0.2, 0.2, 0.4]),
        'age': np.random.normal(40, 12, n_samples).clip(18, 80),
        'Region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate LTV and DTIR
    df['LTV'] = (df['loan_amount'] / df['property_value'] * 100).clip(0, 120)
    df['dtir1'] = np.random.normal(30, 10, n_samples).clip(5, 60)
    
    # Create target variable based on risk factors
    risk_score = np.zeros(n_samples)
    
    # Credit score impact
    risk_score += np.where(df['Credit_Score'] < 600, 0.4, 
                  np.where(df['Credit_Score'] < 700, 0.2, 0))
    
    # DTI impact
    risk_score += np.where(df['dtir1'] > 43, 0.3, 
                  np.where(df['dtir1'] > 36, 0.15, 0))
    
    # LTV impact
    risk_score += np.where(df['LTV'] > 90, 0.25, 
                  np.where(df['LTV'] > 80, 0.1, 0))
    
    # Credit worthiness impact
    credit_worth_map = {'Poor': 0.3, 'Fair': 0.15, 'Good': 0.05, 'Excellent': 0}
    risk_score += df['Credit_Worthiness'].map(credit_worth_map)
    
    # Income to loan ratio impact
    income_ratio = df['loan_amount'] / df['income']
    risk_score += np.where(income_ratio > 5, 0.2, 
                  np.where(income_ratio > 3, 0.1, 0))
    
    # Add some randomness
    risk_score += np.random.normal(0, 0.1, n_samples)
    
    # Convert to binary target (1 = default, 0 = no default)
    df['Status'] = (risk_score > 0.5).astype(int)
    
    return df

def train_model_with_data(dataset_path=None):
    """Train the model with provided dataset or sample data"""
    predictor = LoanDefaultPredictor()
    
    if dataset_path and os.path.exists(dataset_path):
        print(f"Loading dataset from {dataset_path}")
        df = pd.read_csv(dataset_path)
    else:
        print("Creating sample dataset for training...")
        df = create_sample_dataset()
        # Save sample dataset for reference
        df.to_csv('sample_loan_dataset.csv', index=False)
        print("Sample dataset saved as 'sample_loan_dataset.csv'")
    
    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution:")
    print(df['Status'].value_counts())
    print(f"Default rate: {df['Status'].mean():.2%}")
    
    # Train the model
    accuracy = predictor.train(df)
    
    # Save the trained model
    predictor.save_model('loan_model.pkl')
    
    print(f"\nModel training completed with accuracy: {accuracy:.4f}")
    print("Model saved as 'loan_model.pkl'")
    
    # Test with a sample prediction
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
    
    print("\nTesting with sample data:")
    result = predictor.predict(sample_data)
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.1f}%")
    print(f"Risk factors: {result['risk_factors']}")
    print(f"Recommendation: {result['recommendation']}")
    
    return predictor

if __name__ == "__main__":
    import sys
    
    # Check if dataset path is provided as command line argument
    dataset_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("Loan Default Prediction Model Training")
    print("=" * 50)
    
    if dataset_path:
        print(f"Using provided dataset: {dataset_path}")
    else:
        print("No dataset provided. Using sample data for demonstration.")
        print("To use your own dataset, run: python train_model.py path/to/your/dataset.csv")
    
    try:
        predictor = train_model_with_data(dataset_path)
        print("\nTraining completed successfully!")
        print("You can now use the trained model for predictions.")
        
    except Exception as e:
        print(f"Error during training: {str(e)}")
        print("Please check your dataset format and try again.")

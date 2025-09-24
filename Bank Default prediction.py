import pandas as pd
import numpy as np

# === 1. Load Dataset ===
df = pd.read_csv('/Users/Director HR/Downloads/Loan_Default_final (1).csv')

print("=== Original Data ===")
print(df.head())
print("\nShape:", df.shape)

# === 2. Handle Missing Values ===
df.dropna(how='all', inplace=True)

# number columns with median
for col in df.select_dtypes(include=['int64', 'float64']).columns:
    df[col].fillna(df[col].median(), inplace=True)

# categorical columns with mode
for col in df.select_dtypes(include=['object']).columns:
    df[col].fillna(df[col].mode()[0], inplace=True)

# === 3. Remove Duplicates ===
df.drop_duplicates(inplace=True)

# === 4. Fix Data Types (Example) ===
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

# === 5. Rename Columns (Optional) ===
df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"), inplace=True)

# === 6. Remove Outliers (Example using IQR) ===
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower) & (df[col] <= upper)]

# === 7. Save Cleaned Dataset ===
df.to_csv("cleaned_data.csv", index=False)

print("\n=== Cleaned Data ===")
print(df)
print("\nNew Shape:", df.shape)
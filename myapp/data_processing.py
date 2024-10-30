import os
import pandas as pd
import numpy as np

def infer_and_convert_data_types(df):
    for col in df.columns:
        if col == 'Name':
            # Ensure 'Name' column is treated as string
            df[col] = df[col].astype(str)
        elif col == 'Grade':
            # Replace 'Not Available' with NaN
            df[col] = df[col].replace('Not Available', np.nan)
            # Ensure 'Grade' column is treated as string
            df[col] = df[col].astype(str)
        else:
            # Attempt to convert to numeric first
            df_converted = pd.to_numeric(df[col], errors='coerce')
            if not df_converted.isna().all():  # If at least one value is numeric
                df[col] = df_converted
                continue

            # Attempt to convert to datetime with explicit format
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce', format='%d/%m/%Y')
                continue
            except (ValueError, TypeError):
                pass

            # Check if the column should be categorical
            if len(df[col].unique()) / len(df[col]) < 0.5:  # Example threshold for categorization
                df[col] = pd.Categorical(df[col])

    return df

def process_uploaded_file(file_obj):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_obj)

    # Perform data type inference and conversion
    df = infer_and_convert_data_types(df)

    # Convert DataFrame to JSON
    try:
        json_data = df.to_json(orient='records')
        return json_data
    except ValueError as e:
        return {"error": str(e)}

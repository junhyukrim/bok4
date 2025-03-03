import os
import pandas as pd
import re

# Step 1: Define the folder containing the CSV files
folder_path = "C:/Users/egege/OneDrive/Documents/bok4_resource/bond_csv"

# Step 2: Define a function to extract and convert the date from doc_id
def convert_date(doc_id):
    # Find the first occurrence of 6 consecutive digits
    match = re.search(r'\d{6}', doc_id)
    if match:
        yymmdd = match.group()
        yyyy = '20' + yymmdd[:2]  # Add '20' to the year
        mmdd = yymmdd[2:]  # Keep the month and day
        return yyyy + mmdd
    return "Unknown Date"  # Return this if no match is found

# Step 3: Process all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):  # Check if the file is a CSV
        file_path = os.path.join(folder_path, file_name)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Apply the date conversion function to update the 'date' column
        df['date'] = df['doc_id'].apply(convert_date)
        
        # Overwrite the existing CSV file with updated data
        df.to_csv(file_path, index=False)

print("All CSV files in the folder have been processed and updated.")

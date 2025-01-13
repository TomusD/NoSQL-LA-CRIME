import pandas as pd

# Load the original CSV file
input_file = "F:/github/NoSQL-LA-CRIME/Crime_Data_from_2020_to_Present_20241025_clean.csv"
output_file = "first_100_rows.csv"

# Read the CSV file
df = pd.read_csv(input_file)

# Clean date columns with explicit format specification
date_format = '%m/%d/%Y %I:%M:%S %p'  # Format for "03/01/2020 12:00:00 AM"
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'], format=date_format).dt.strftime('%m/%d/%Y')
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'], format=date_format).dt.strftime('%m/%d/%Y')

# Keep only the first 100 rows
df_first_100 = df.head(100)

# Save the first 100 rows to a new CSV file
df_first_100.to_csv(output_file, index=False)

print(f"First 100 rows have been saved to '{output_file}'")
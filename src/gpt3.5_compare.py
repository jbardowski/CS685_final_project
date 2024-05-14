import os
import pandas as pd

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the raw documents folder
baseline_files_path = os.path.join(script_dir, "baseline_files")

FILENAME = 'gpt35.csv'
file_path = os.path.join(baseline_files_path, FILENAME)
df = pd.read_csv(file_path)

# Print the count of 'yes' and 'no' values for the 'scope3' column
print("Number of 'yes' and 'no' values in 'scope3' column:")
print(df['scope3'].value_counts())
print()

# Print the count of 'yes' and 'no' values for the 'scope3_new' column
print("Number of 'yes' and 'no' values in 'scope3_new' column:")
print(df['scope3_new'].value_counts())
print()

accuracy = (df['scope3'] == df['scope3_new']).mean() * 100
print(f"Accuracy: {accuracy:.2f}%")
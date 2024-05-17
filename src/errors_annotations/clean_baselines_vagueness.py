import pandas as pd
import os

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the raw documents folder
baseline_files_path = os.path.join(script_dir, "baseline_files")

# FILENAME = 'mistral7b_baseline_new.csv'
FILENAME = 'mistral7b_baseline_new.csv'

# Read the CSV file
file_path = os.path.join(baseline_files_path, FILENAME)
df = pd.read_csv(file_path)

# Define a dictionary to map the values in the 'vague' column
vague_mapping = {
    'ambiguous': ['ambiguous'],
    'generic': ['generic'],
    'notESG': ['notESG', 'not related'],
    'specific': ['specific']
}

# Function to compare the values and return the result
def compare_values(vague_value, chat_response_value):
    chat_response_value = chat_response_value.lower().split('-')[0].strip()
    chat_response_value = chat_response_value.replace('1.', '').replace('2.', '').replace('3.', '').replace('4.', '').strip()
    if chat_response_value in vague_mapping.get(vague_value, []):
        return 'match'
    elif any(value in chat_response_value for value in ['ambiguous', 'generic', 'notESG', 'specific', 'not related']):
        return 'no match'
    else:
        return 'undefined'

# Apply the comparison function to the DataFrame
df['result'] = df.apply(lambda row: compare_values(row['vague'], row['chat_response_vague']), axis=1)

# Save the updated DataFrame to a new CSV file
output_file_path = os.path.join(baseline_files_path, "processed_" + FILENAME)
df.to_csv(output_file_path, index=False)

print(f"Processed file saved to: {output_file_path}")

# Calculate metrics
total_rows = len(df)
num_matches = df['result'].value_counts().get('match', 0)
num_no_matches = df['result'].value_counts().get('no match', 0)
num_undefined = df['result'].value_counts().get('undefined', 0)
accuracy = (num_matches / total_rows) * 100

print(f"\nMetrics:")
print(f"Total rows: {total_rows}")
print(f"Number of matches: {num_matches}")
print(f"Number of no matches: {num_no_matches}")
print(f"Number of undefined: {num_undefined}")
print(f"Accuracy: {accuracy:.2f}%")
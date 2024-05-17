import pandas as pd
from collections import defaultdict

# Read the CSV file
df = pd.read_csv('decoder_test_results.csv')

# Create a dictionary to store the error counts
error_counts = defaultdict(int)

# Initialize variables for accuracy metrics
total_count = 0
correct_count = 0

# Create lists to store accurate and discrepancy results
accurate_results = []
discrepancy_results = []

# Iterate over the rows
for i, row in df.iterrows():
    text = row['text']
    vague = row['vague']
    predicted_vague = row['predicted_vague']

    total_count += 1

    # Check if the prediction is correct
    if vague == predicted_vague:
        correct_count += 1
        accurate_results.append({'text': text, 'vague': vague, 'predicted_vague': predicted_vague})
        continue

    # If the prediction is incorrect, update the error count
    error_key = f"{vague} -> {predicted_vague}"
    error_counts[error_key] += 1
    discrepancy_results.append({'text': text, 'vague': vague, 'predicted_vague': predicted_vague})

# Calculate accuracy metrics
accuracy = correct_count / total_count
error_rate = 1 - accuracy

# Print the accuracy metrics
print("Accuracy Metrics:")
print("------------------")
print(f"Total samples: {total_count}")
print(f"Correct predictions: {correct_count}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Error rate: {error_rate:.4f}")
print()

# Print the error analysis
print("Error Analysis:")
print("----------------")
for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{error}: {count}")

# Create DataFrames from the lists
accurate_df = pd.DataFrame(accurate_results)
discrepancy_df = pd.DataFrame(discrepancy_results)

# Save the DataFrames as CSV files
accurate_df.to_csv('accurate_results.csv', index=False)
discrepancy_df.to_csv('discrepancy_results.csv', index=False)
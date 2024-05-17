import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the processed files
processed_files_path = script_dir

# Load the processed data files
gemma2b_df = pd.read_csv(os.path.join(processed_files_path, "processed_gemma2b_baseline_new.csv"))
gemma7b_df = pd.read_csv(os.path.join(processed_files_path, "processed_gemma7b_baseline_new.csv"))
mistral7b_df = pd.read_csv(os.path.join(processed_files_path, "processed_mistral7b_baseline_new.csv"))

# Function to extract accuracy, precision, recall, and F1-score from a DataFrame
def extract_metrics(df, model_name):
    accuracy = (df['scope3'] == df[model_name]).mean() * 100
    return accuracy

# Extract metrics for each model
gemma2b_metrics = extract_metrics(gemma2b_df, 'gemma2b_baseline')
gemma7b_metrics = extract_metrics(gemma7b_df, 'gemma7b_baseline')
mistral7b_metrics = extract_metrics(mistral7b_df, 'mistral7b_baseline')

# Create a DataFrame for model comparison
model_comparison = pd.DataFrame({
    'Model': ['gemma2b', 'gemma7b', 'mistral7b'],
    'Accuracy': [gemma2b_metrics, gemma7b_metrics, mistral7b_metrics]
})

# Create a bar-marker plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.set_style("whitegrid")

# Plot the bar markers
ax = sns.barplot(x='Model', y='Accuracy', data=model_comparison)

# Customize the chart
ax.set_xlabel('Model', fontsize=14)
ax.set_ylabel('Accuracy (%)', fontsize=14)
ax.set_title('Accuracy Comparison', fontsize=16, fontweight='bold')

# Add value labels
for i, accuracy in enumerate(model_comparison['Accuracy']):
    ax.text(i, accuracy + 0.5, f"{accuracy:.2f}%", ha='center', va='bottom', fontsize=12)

plt.show()
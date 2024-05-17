import pandas as pd
import csv
import os
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, classification_report
import string
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the raw documents folder
baseline_files_path = os.path.join(script_dir, "baseline_files")

scope3_categories = ["Purchased goods and services",
                    "Capital goods",
                    "Fuel and energy-related activities",
                    "Upstream transportation and distribution",
                    "Waste generated in operations",
                    "Business travel",
                    "Employee commuting",
                    "Upstream leased assets",
                    "Downstream transportation and distribution",
                    "Processing of sold products",
                    "Use of sold products",
                    "End-of-life treatment of sold products",
                    "Downstream leased assets",
                    "Franchises",
                    "Investments"]

def process_chat_response(response):
    response_cleaned = response.translate(str.maketrans('', '', string.punctuation))
    response_lower = response_cleaned.lower()
    if any(category.lower() in response_lower and "no" not in response_lower and "not" not in response_lower for category in scope3_categories):
        return "yes"
    elif ("yes" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("sentence is disc" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("sentence disc" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("falls into the category of scope 3 emissions" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("it is a scope 3 emissions sentence" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("therefore, the category of scope 3 is " in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("is discussing scope 3 emissions"in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("discusses scope 3 emissions" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("does discuss scope 3 emissions" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("is discussing" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("sentence is indeed discussing" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("is related" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("discussion is related to scope" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("discussion is about" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("discussion is focused" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("discussion is indeed" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("appears to be disc" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("discussion includes scope 3 emissions" in response_lower and "no" not in response_lower and "not" not in response_lower) or \
         ("yes the sentence is discussing scope 3 emissions" in response_lower) or \
         ("does mention scope 3 emissions" in response_lower and "no" not in response_lower and "not" not in response_lower):
        return "yes"
    # elif "no," in response_lower or "does not" in response_lower or \
    #      "is not" in response_lower or \
    #      "none" in response_lower or \
    #      "emissions are not" in response_lower or \
    #      "cannot " in response_lower or \
    #      "there is no" in response_lower:
    #     return "no"
    else:
        return "no"

if __name__ == "__main__":
    # FILENAME = 'gemma2b_baseline_new.csv'
    # FILENAME = 'gemma7b_baseline_new.csv'
    FILENAME = 'mistral7b_baseline_new.csv'
    # FILENAME = 'test_mistral.csv'
    file_path = os.path.join(baseline_files_path, FILENAME)
    df = pd.read_csv(file_path)

    df[FILENAME.split("_new")[0]] = df["chat_response_scope3"].apply(process_chat_response)

    # Print number of 'yes' and 'no' values in 'scope3' column and the newly created column
    print("Number of 'yes' and 'no' values in 'scope3' column:")
    print(df['scope3'].value_counts())
    print("\nNumber of 'yes' and 'no' values in the newly created column:")
    print(df[FILENAME.split("_new")[0]].value_counts())

    # Calculate accuracy
    accuracy = (df['scope3'] == df[FILENAME.split("_new")[0]]).mean() * 100
    print(f"\nAccuracy: {accuracy:.2f}%")

    # Calculate precision, recall, and F1-score
    precision = precision_score(df['scope3'], df[FILENAME.split("_new")[0]], pos_label='yes')
    recall = recall_score(df['scope3'], df[FILENAME.split("_new")[0]], pos_label='yes')
    f1 = f1_score(df['scope3'], df[FILENAME.split("_new")[0]], pos_label='yes')
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")

    # Plot precision, recall, and F1-score
    metrics = [precision, recall, f1]
    metric_names = ['Precision', 'Recall', 'F1-score']
    x_pos = np.arange(len(metric_names))

    plt.figure(figsize=(8, 6))
    plt.bar(x_pos, metrics, align='center', alpha=0.5)
    plt.xticks(x_pos, metric_names)
    plt.ylabel('Score')
    plt.title('Precision, Recall, and F1-score')
    plt.ylim([0, 1])
    plt.show()

    # Calculate confusion matrix
    confusion_mat = confusion_matrix(df['scope3'], df[FILENAME.split("_new")[0]], labels=['no', 'yes'])
    print("\nConfusion Matrix:")
    print(confusion_mat)

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(confusion_mat, annot=True, cmap='Blues', fmt='g', cbar=False)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')
    plt.show()

    # Generate classification report
    report = classification_report(df['scope3'], df[FILENAME.split("_new")[0]], target_names=['no', 'yes'], output_dict=True)
    report_df = pd.DataFrame(report).transpose()

    # Plot classification report
    plt.figure(figsize=(8, 6))
    sns.heatmap(report_df, annot=True, cmap='Blues', fmt='.2f', cbar=False)
    plt.xlabel('Metrics')
    plt.ylabel('Classes')
    plt.title('Classification Report')
    plt.show()

    df.to_csv("processed_" + FILENAME, quoting=csv.QUOTE_ALL, index=False)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
data = pd.read_csv('manual_annotation.csv', encoding='latin1')

# Preprocess the data
# data['decoder_model_output'] = data['decoder_model_output'].replace({'ambiguous': 0, 'generic': 1, 'notESG': 2, 'specific': 3})
# data['manual_annotation'] = data['manual_annotation'].replace({'ambiguous': 0, 'generic': 1, 'notESG': 2, 'specific': 3})

# Reset the index to ensure the labels match
data = data.reset_index(drop=True)

# # Create a confusion matrix
# confusion_matrix = pd.crosstab(data['manual_annotation'], data['decoder_model_output'], rownames=['Actual'], colnames=['Predicted'])
# plt.figure(figsize=(8, 6))
# sns.heatmap(confusion_matrix, annot=True, cmap="Blues", fmt="d")
# plt.title("Confusion Matrix")
# plt.xlabel("Predicted")
# plt.ylabel("Actual")
# plt.show()

label_map = {0: 'ambiguous', 1: 'generic', 2: 'notESG', 3: 'specific'}

# Plot the distribution of predictions and ground truth
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.title("Predicted Distribution")
data['decoder_model_output'].value_counts().sort_index().plot(kind='bar')

plt.subplot(1, 2, 2)
plt.title("Ground Truth Distribution")
data['manual_annotation'].value_counts().sort_index().plot(kind='bar')

plt.tight_layout()
plt.show()

# Plot the accuracy for each category
accuracy_by_category = data.groupby('manual_annotation')['decoder_model_output'].apply(lambda x: sum(x == data['manual_annotation']) / len(x))
accuracy_by_category.plot(kind='bar', title='Accuracy by Category')
plt.xlabel('Category')
plt.ylabel('Accuracy')
plt.show()
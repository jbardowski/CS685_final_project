import pandas as pd
import matplotlib.pyplot as plt
import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import sent_tokenize, word_tokenize, pos_tag

# Load the data
# data = pd.read_csv('decoder_discrepancies.csv')

data = pd.read_csv('decoder_test_results_cleaned.csv')

# Compute errors
data['error'] = (data['gpt4_annotation'] != data['predicted_annotation']).astype(int)

# Error Analysis by Semantic Category
# Define semantic categories
semantic_categories = {
    'Environmental Initiatives': ['environment', 'sustainability', 'climate', 'emission', 'renewable', 'energy', 'carbon', 'footprint'],
    'Supply Chain': ['supply', 'chain', 'supplier', 'manufacturing'],
    'Goals and Targets': ['goal', 'target', 'ambition'],
    'Partnerships': ['partner', 'joint', 'venture'],
    'Other': []
}



# Assign semantic categories
data['semantic_category'] = 'Other'
for category, keywords in semantic_categories.items():
    for keyword in keywords:
        data.loc[data['sentence'].str.lower().str.contains(keyword), 'semantic_category'] = category

# Stacked bar chart for error distribution across semantic categories
category_errors = data.groupby('semantic_category')['error'].sum()
category_totals = data.groupby('semantic_category')['error'].count()

fig, ax = plt.subplots(figsize=(10, 6))
category_errors.plot(kind='bar', ax=ax)

# Rotate x-axis labels and adjust spacing
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.3)

plt.title('Error Distribution across Semantic Categories')
plt.xlabel('Semantic Category')
plt.ylabel('Number of Errors')

plt.tight_layout()
plt.show()

# Error Analysis by Syntactic Complexity
# Compute sentence lengths
data['sentence_length'] = data['sentence'].apply(lambda x: len(word_tokenize(x)))

# Compute number of clauses
def count_clauses(sentence):
    tokens = word_tokenize(sentence)
    tags = pos_tag(tokens)
    clauses = 0
    for i, (word, tag) in enumerate(tags):
        if tag.startswith('VB') and (i == 0 or tags[i-1][1] != 'CC'):
            clauses += 1
    return clauses

data['num_clauses'] = data['sentence'].apply(count_clauses)

# Plot error distribution by sentence length
plt.figure(figsize=(10, 6))
plt.hist([data[data['error'] == 1]['sentence_length'], data[data['error'] == 0]['sentence_length']], bins=20, label=['Errors', 'Correct'], stacked=True)
plt.title('Error Distribution by Sentence Length')
plt.xlabel('Sentence Length')
plt.ylabel('Number of Sentences')
plt.legend()
plt.show()

# Plot error distribution by number of clauses
plt.figure(figsize=(10, 6))
plt.hist([data[data['error'] == 1]['num_clauses'], data[data['error'] == 0]['num_clauses']], bins=10, label=['Errors', 'Correct'], stacked=True)
plt.title('Error Distribution by Number of Clauses')
plt.xlabel('Number of Clauses')
plt.ylabel('Number of Sentences')
plt.legend()
plt.show()
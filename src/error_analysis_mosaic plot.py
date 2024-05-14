import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag

# Load the data
data = pd.read_csv('decoder_discrepancies.csv')

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

# Violin plot for error distribution across semantic categories
plt.figure(figsize=(10, 6))
sns.violinplot(x='semantic_category', y='error', data=data, inner='box')
plt.title('Error Distribution across Semantic Categories')
plt.xlabel('Semantic Category')
plt.ylabel('Error')
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

# Box plot for error distribution by sentence length
plt.figure(figsize=(10, 6))
sns.boxplot(x='error', y='sentence_length', data=data)
plt.title('Error Distribution by Sentence Length')
plt.xlabel('Error')
plt.ylabel('Sentence Length')
plt.show()

# Box plot for error distribution by number of clauses
plt.figure(figsize=(10, 6))
sns.boxplot(x='error', y='num_clauses', data=data)
plt.title('Error Distribution by Number of Clauses')
plt.xlabel('Error')
plt.ylabel('Number of Clauses')
plt.show()
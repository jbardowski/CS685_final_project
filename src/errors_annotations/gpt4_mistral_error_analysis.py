import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('processed_mistral7b_baseline_new.csv')

disagreements_gpt4_yes_mistral_no = []
disagreements_gpt4_no_mistral_yes = []

for idx, row in df.iterrows():
    sentence = row['text']
    gpt4_annotation = row['scope3']
    mistral_annotation = row['mistral7b_baseline']
    mistral_response = row['chat_response_scope3']

    if (gpt4_annotation != mistral_annotation):
        disagreement = {
            'sentence': sentence,
            'gpt4_annotation': gpt4_annotation,
            'mistral_annotation': mistral_annotation,
            'mistral_response': mistral_response
        }
        if (gpt4_annotation == 'yes') and (mistral_annotation == 'no'):
            disagreements_gpt4_yes_mistral_no.append(disagreement)
        elif (gpt4_annotation == 'no') and (mistral_annotation == 'yes'):
            disagreements_gpt4_no_mistral_yes.append(disagreement)

disagreements_gpt4_yes_mistral_no_df = pd.DataFrame(disagreements_gpt4_yes_mistral_no)
disagreements_gpt4_no_mistral_yes_df = pd.DataFrame(disagreements_gpt4_no_mistral_yes)

print("Instances where GPT-4 is 'yes' and Mistral7b is 'no':")
print(disagreements_gpt4_yes_mistral_no_df)
print("\nInstances where GPT-4 is 'no' and Mistral7b is 'yes':")
print(disagreements_gpt4_no_mistral_yes_df)

disagreements_gpt4_yes_mistral_no_df.to_csv('disagreements_gpt4_yes_mistral_no.csv', index=False)
disagreements_gpt4_no_mistral_yes_df.to_csv('disagreements_gpt4_no_mistral_yes.csv', index=False)


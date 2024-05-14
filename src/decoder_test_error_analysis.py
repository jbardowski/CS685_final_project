import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('decoder_test_results.csv')

disagreements_gpt4_yes_predicted_no = []
disagreements_gpt4_no_predicted_yes = []

for idx, row in df.iterrows():
    sentence = row['text']
    gpt4_annotation = row['scope3']
    predicted_annotation = row['predicted_scope3']

    if (gpt4_annotation != predicted_annotation):
        disagreement = {
            'sentence': sentence,
            'gpt4_annotation': gpt4_annotation,
            'predicted_annotation': predicted_annotation
        }

        if (gpt4_annotation == 'yes') and (predicted_annotation == 'no'):
            disagreements_gpt4_yes_predicted_no.append(disagreement)
        elif (gpt4_annotation == 'no') and (predicted_annotation == 'yes'):
            disagreements_gpt4_no_predicted_yes.append(disagreement)

disagreements_gpt4_yes_predicted_no_df = pd.DataFrame(disagreements_gpt4_yes_predicted_no)
disagreements_gpt4_no_predicted_yes_df = pd.DataFrame(disagreements_gpt4_no_predicted_yes)

print("Instances where GPT-4 is 'yes' and predicted_scope3 is 'no':")
print(disagreements_gpt4_yes_predicted_no_df)
print("\nInstances where GPT-4 is 'no' and predicted_scope3 is 'yes':")
print(disagreements_gpt4_no_predicted_yes_df)

disagreements_gpt4_yes_predicted_no_df.to_csv('disagreements_gpt4_yes_predicted_no.csv', index=False)
disagreements_gpt4_no_predicted_yes_df.to_csv('disagreements_gpt4_no_predicted_yes.csv', index=False)
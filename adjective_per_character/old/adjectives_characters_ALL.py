import os
import spacy
import csv
from collections import Counter

# Set a larger field size limit
csv.field_size_limit(10**8)  # Set the field size limit to 100 MB (adjust as needed)

# Define 'input_folder' and 'output_folder'
input_folder = 'input_folder'
output_folder = 'output_folder'

# Load the SpaCy model outside the main function
nlp = spacy.load("fr_core_news_sm")

def extract_adjectives_for_persons(names, text, nlp_model):
    result_data = []

    # Extract adjectives 
    doc = nlp(text)

    # Create a dictionary to store unique adjectives for each person
    people_dict = {name: set() for name in names}

    for name in names:
        # Use the doc to find matches in the text
        matches = [token.text.lower() for token in doc if token.text.lower() == name.lower()]
        for match in matches:
            # Find unique adjectives in a broader context around the matched name
            adjectives = {word.text.lower() for token in doc for word in token.subtree if word.pos_ == 'ADJ' and token.text.lower() == match}

            # Exclude the character name itself from the set of adjectives
            adjectives.discard(name.lower())

            # Add unique adjectives to the corresponding person's set
            people_dict[name].update(adjectives)

    # Extract the top three adjectives for each character name along with their counts
    for name, adjectives in people_dict.items():
        adjective_counter = Counter(adjectives)
        top_adjectives = adjective_counter.most_common(3)
        result_data.append({
            'character': name,
            'Adjectives': ', '.join([adj for adj, _ in top_adjectives]),
            'Adjective_Counts': ', '.join([str(adjective_counter[adj]) for adj, _ in top_adjectives])
        })

    return result_data

def save_to_tsv(output_tsv, data):
    with open(output_tsv, 'w', encoding='utf-8', newline='') as tsvfile:
        fieldnames = ['character', 'Adjectives', 'Adjective_Counts']
        writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
        
        writer.writeheader()
        writer.writerows(data)

def process_files(input_folder, output_folder, nlp_model):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.tsv'):
            # Define input and output paths for each file
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace('.tsv', '_results.tsv'))

            with open(input_path, 'r', encoding='utf-8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                next(reader, None)  # Skip the header

                for row in reader:
                    # Ensure the row has enough elements
                    if len(row) >= 2:
                        # Extract character names and text
                        names = row[0].split(',')
                        text = row[1]

                        # Extract adjectives for each person name using the new logic
                        result_data = extract_adjectives_for_persons(names, text, nlp_model)

                        # Save results to TSV
                        save_to_tsv(output_path, result_data)

# Call the function to process files in the input folder
process_files(input_folder, output_folder, nlp)

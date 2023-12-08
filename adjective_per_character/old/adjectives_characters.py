from collections import Counter

import spacy
import csv

# Replace 'character_text.tsv' and 'output_results.tsv' with the actual file names
input_tsv = 'character_text.tsv'
output_tsv = 'output_results.tsv'

# Load the SpaCy model outside the main function
nlp = spacy.load("fr_core_news_sm")

def extract_adjectives_for_persons(names, text, nlp_model):
    result_data = []
    
    # Extract adjectives using the provided logic
    doc = nlp(text)
    people_dict = {name: [] for name in names}

    for name in names:
        # Use the doc to find matches in the text
        matches = [token.text.lower() for token in doc if token.text.lower() == name.lower()]
        for match in matches:
            # Find adjectives in the same sentence as the matched name
            sentence = [token for token in doc if token.text.lower() == match][0].sent
            adjectives = [word.text.lower() for word in sentence if word.pos_ == 'ADJ']
            people_dict[name].extend(adjectives)

    # Select the top three most frequent adjectives for each character
    for character_name in names:
        adjectives_counter = Counter(people_dict.get(character_name, []))
        top_three_adjectives = adjectives_counter.most_common(3)
        result_data.append({'character': character_name, 'Adjectives': ', '.join([adj[0] for adj in top_three_adjectives])})

    return result_data

def save_to_tsv(output_tsv, data):
    with open(output_tsv, 'w', encoding='utf-8', newline='') as tsvfile:
        fieldnames = ['character', 'Adjectives']
        writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
        
        writer.writeheader()
        writer.writerows(data)

def main(input_tsv, output_tsv, nlp_model):
    with open(input_tsv, 'r', encoding='utf-8') as tsvfile:
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
                save_to_tsv(output_tsv, result_data)

# Call the main function
main(input_tsv, output_tsv, nlp)

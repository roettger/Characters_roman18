import spacy
import csv
from collections import Counter

# Replace 'character_text.tsv' and 'output_results.tsv' with the actual file names
input_tsv = 'character_text.tsv'
output_tsv = 'output_results.tsv'

# Load the SpaCy model outside the main function
nlp = spacy.load("fr_core_news_sm")

def extract_top_adjectives_for_character(character_name, text, nlp_model, top_n=5):
    doc = nlp_model(text)
    adjectives = [token.text.lower() for token in doc if token.pos_ == "ADJ"]
    adjective_counts = Counter(adjectives)
    top_adjectives = [adj for adj, count in adjective_counts.most_common(top_n)]
    return {'character': character_name, 'Top Adjectives': ', '.join(top_adjectives)}

def save_to_tsv(output_tsv, data):
    with open(output_tsv, 'w', encoding='utf-8', newline='') as tsvfile:
        fieldnames = ['character', 'Top Adjectives']
        writer = csv.DictWriter(tsvfile, fieldnames=fieldnames, delimiter='\t')
        
        writer.writeheader()
        writer.writerows(data)

def main(input_tsv, output_tsv, nlp_model):
    result_data = []

    with open(input_tsv, 'r', encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        next(reader)  # Skip the header

        for row in reader:
            # Extract character names and text
            characters_and_text = row[0].split('\t')
            character_names = [name.strip() for name in characters_and_text[0].split(',')]
            text = characters_and_text[1]

            # Extract top 5 adjectives for each character
            for character_name in character_names:
                result_data.append(extract_top_adjectives_for_character(character_name, text, nlp_model))

    # Save results to TSV
    save_to_tsv(output_tsv, result_data)

# Call the main function
main(input_tsv, output_tsv, nlp)

import os
import re
import nltk
from bs4 import BeautifulSoup

# Download NLTK's Punkt tokenizer data
nltk.download('punkt')

def clean_wikipedia_article_preserve_paragraphs(raw_text):
    # Step 1: Remove HTML tags if any
    soup = BeautifulSoup(raw_text, "html.parser")
    text = soup.get_text()

    # Step 2: Remove sections like 'See also', 'References', 'External links' but keep the paragraph flow
    text = re.sub(r'== *(See also|References|External links|Further reading) *==.*', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Step 3: Remove inline references like [1], [2], [citation needed]
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\[citation needed\]', '', text, flags=re.IGNORECASE)

    # Step 4: Handle Wikipedia-style links [[Page Title|display text]] or [[Page Title]]
    text = re.sub(r'\[\[([^|\]]+)\|([^|\]]+)\]\]', r'\2', text)  # Replace [[Page Title|display text]] with 'display text'
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)  # Replace [[Page Title]] with 'Page Title'

    # Step 5: Remove bold and italics markers (e.g., '''bold''' or ''italic'')
    text = re.sub(r"'''(.*?)'''", r'\1', text)  # Remove triple quotes
    text = re.sub(r"''(.*?)''", r'\1', text)    # Remove double quotes

    # Step 6: Remove redundant newlines but keep paragraph structure intact
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Preserve paragraph structure by keeping double newlines

    # Step 7: Fix multiple spaces or inconsistent spacing
    text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space

    # Step 8: Format sentences to ensure each starts with a capital letter
    sentences = nltk.sent_tokenize(text)
    formatted_text = "\n".join(sentences)

    return formatted_text

# Step 1: Load all documents, clean them, and save the results
def process_wikipedia_articles(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder, filename)

            # Read the content of the file
            with open(input_file_path, 'r', encoding='utf-8') as file:
                raw_text = file.read()

            # Clean the content using the function
            cleaned_text = clean_wikipedia_article_preserve_paragraphs(raw_text)

            # Write the cleaned text to a new file in the output folder
            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

    print(f"All files in '{input_folder}' have been processed and saved to '{output_folder}'.")

# Specify the folder paths
input_folder_path = r"C:\Users\Junaid Ur Rehman\Documents\Master of Business Analytics\Semester 5\Applications of Data Science\Final Project\random_wikipedia_articles"
output_folder_path = r"C:\Users\Junaid Ur Rehman\Documents\Master of Business Analytics\Semester 5\Applications of Data Science\Final Project\processed_wikipedia_articles"

# Step 2: Process all Wikipedia articles in the input folder
process_wikipedia_articles(input_folder_path, output_folder_path)

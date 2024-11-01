import os
import random
import nltk

# Download NLTK's Punkt tokenizer data if not already downloaded
nltk.download('punkt')

# Step 1: Load all documents from the specified folder
def load_documents_from_folder(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append(content)
    return documents

# Step 2: Tokenize documents into sentences and prepare segments with boundary markers
def create_segments_with_markers(documents, num_segments=50, sentence_range=(3, 5)):
    segments = []

    for _ in range(num_segments):
        segment = []
        selected_docs = random.sample(documents, 10)  # Randomly select 10 documents

        for i, doc in enumerate(selected_docs):
            # Tokenize the document into sentences
            sentences = nltk.sent_tokenize(doc)
            # Randomly select a number of sentences from the range (3 to 5)
            num_sentences = random.randint(*sentence_range)
            selected_sentences = random.sample(sentences, min(num_sentences, len(sentences)))
            # Add the selected sentences to the segment
            segment.extend(selected_sentences)

            # Add a boundary marker to indicate where the current document ends
            if i < len(selected_docs) - 1:  # Don't add the marker after the last document
                segment.append("\n==========\n")  # Add a visual boundary marker

        # Concatenate all selected sentences to form a single segment
        segments.append("\n".join(segment))

    return segments

# Step 3: Load documents from the specified folder
folder_path = r"C:\Users\Junaid Ur Rehman\Documents\Master of Business Analytics\Semester 5\Applications of Data Science\Final Project\processed_wikipedia_articles"
documents = load_documents_from_folder(folder_path)

# Step 4: Create segments similar to the Choi dataset from the loaded Wikipedia documents with range (3, 5)
segments = create_segments_with_markers(documents, num_segments=50, sentence_range=(3, 5))

# Step 5: Save each segment into separate text files
output_folder = r"C:\Users\Junaid Ur Rehman\Documents\Master of Business Analytics\Semester 5\Applications of Data Science\Final Project\final_wikipedia"
os.makedirs(output_folder, exist_ok=True)

# Save each segment into a separate file with the ".ref" extension
for i, segment in enumerate(segments):
    output_file_path = os.path.join(output_folder, f"segment_{i+1}.ref")  # Change extension to .ref
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(segment)

print(f"Total segments created and saved as separate .ref files: {len(segments)}")


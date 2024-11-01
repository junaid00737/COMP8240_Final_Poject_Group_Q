import requests
import os
import time

# Function to download random Wikipedia articles
def download_random_wikipedia_articles(num_articles=100, language='en'):
    base_url = f"https://{language}.wikipedia.org/w/api.php"
    output_folder = "random_wikipedia_articles"
    os.makedirs(output_folder, exist_ok=True)

    for i in range(num_articles):
        try:
            # Get a random article title
            params = {
                "action": "query",
                "format": "json",
                "list": "random",
                "rnnamespace": 0,  # Namespace 0 is for content pages (not talk pages)
                "rnlimit": 1
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            page_title = data['query']['random'][0]['title']
            print(f"Fetching article {i+1}/{num_articles}: {page_title}")

            # Get the page content by title
            params = {
                "action": "query",
                "format": "json",
                "prop": "extracts",
                "explaintext": True,
                "titles": page_title
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            page_data = response.json()
            page = list(page_data['query']['pages'].values())[0]
            content = page.get('extract', '')

            # Save the content to a text file
            if content.strip():  # Only save if content is not empty
                filename = os.path.join(output_folder, page_title.replace(' ', '_') + '.txt')
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Article '{page_title}' saved as '{filename}'")
            else:
                print(f"Article '{page_title}' has no content, skipping.")

            # Add a short delay to avoid overwhelming the Wikipedia API
            time.sleep(0.5)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            time.sleep(2)  # Add a longer delay if there's an error

# Run the function to download 100 random articles
download_random_wikipedia_articles(num_articles=100)

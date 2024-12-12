
'''import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()  # Extract relevant text from the website
    except Exception as e:
        return f"Error scraping website: {e}"'''


import requests
from bs4 import BeautifulSoup

# Function to scrape a website and clean the data
def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Clean HTML by removing unnecessary tags
        for script_or_style in soup(['script', 'style', 'head', 'title', 'meta']):
            script_or_style.decompose()

        return soup.get_text(separator=' ', strip=True)  # Extract relevant text
    except requests.exceptions.RequestException as e:
        return f"Error scraping website: {e}"
import requests
from bs4 import BeautifulSoup
import time
import logging

# Setup logging
logging.basicConfig(filename='scrape_articles.log', level=logging.INFO, format='%(asctime)s %(message)s')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

def scrape_article(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Filtering out unwanted sections (can be adjusted)
        for script in soup(["script", "style"]):
            script.extract()
        
        title = soup.find('h1').text if soup.find('h1') else 'No Title Found'
        content = ' '.join([p.text for p in soup.find_all('p')])
        return title, content
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return None, None

def scrape_articles_from_file(urls_file):
    with open(urls_file, 'r') as file:
        urls = file.readlines()
    articles = []
    for url in urls:
        url = url.strip()
        if url:
            logging.info(f"Scraping content from {url}")
            title, content = scrape_article(url)
            if title and content:
                articles.append((title, content))
            time.sleep(1)  # Add a delay between requests to avoid overloading servers
    return articles

if __name__ == "__main__":
    urls_file = "../data/urls.txt"
    articles = scrape_articles_from_file(urls_file)
    with open("../data/scraped_articles.txt", 'w') as file:
        for title, content in articles:
            file.write(f"Title: {title}\nContent: {content}\n\n")
    print("Scraping completed and articles saved.")
    logging.info("Scraping completed and articles saved.")

import re

# Function to preprocess text
def preprocess(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    return text

# Function to preprocess articles from a file
def preprocess_articles(scraped_file, preprocessed_file):
    with open(scraped_file, 'r', encoding='latin-1') as file:
        articles = file.read().split('\n\n')  # Split articles by double newline
    
    preprocessed_articles = []
    for article in articles:
        if article.strip():
            try:
                if '\nContent: ' in article:
                    parts = article.split('\nContent: ', 1)
                    if len(parts) == 2:
                        title, content = parts
                        title = title.replace('Title: ', '').strip()
                        content = preprocess(content.strip())
                        preprocessed_articles.append((title, content))
                    else:
                        raise ValueError("Article does not contain expected parts")
                else:
                    # Handle articles without 'Title' and 'Content' split
                    lines = article.split('\n')
                    title = lines[0].strip() if lines else "No Title Found"
                    content = preprocess(' '.join(lines[1:]).strip())
                    preprocessed_articles.append((title, content))
            except ValueError as e:
                print(f"Error processing article: {article[:100]}...")  # Log the problematic article
                print(e)
    
    with open(preprocessed_file, 'w', encoding='utf-8') as file:
        for title, content in preprocessed_articles:
            file.write(f"Title: {title}\nContent: {content}\n\n")
    print("Preprocessing completed and articles saved.")

# Main script execution
if __name__ == "__main__":
    scraped_file = "../data/scraped_articles.txt"
    preprocessed_file = "../data/preprocessed_articles.txt"
    preprocess_articles(scraped_file, preprocessed_file)

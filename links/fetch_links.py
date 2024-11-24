import json
import os
import requests
from bs4 import BeautifulSoup
import time

# Function to perform a Google search
def search_google(topic, subject_name, num_results=1):
    query = f"{topic} in {subject_name}"
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for item in soup.select('div.tF2Cxc a'):  # Selector for links
            link = item.get('href')
            if link.startswith("http"):
                links.append(link)
        time.sleep(1)  # Delay between requests to avoid being blocked
        return links[:num_results]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

# Function to perform an advanced fallback search
def fallback_search(topic, subject_name):
    # Additional context words to refine the search
    context_keywords = ["overview", "tutorial", "lecture notes"]
    fallback_links = []

    for keyword in context_keywords:
        refined_query = f"{topic} {keyword} in {subject_name}"
        print(f"Refining search with query: '{refined_query}'")
        refined_links = search_google(refined_query, subject_name, num_results=2)
        if refined_links:
            fallback_links.extend(refined_links)
            break  # Stop if we get any results

    # Additional site-specific search
    site_searches = ["geeksforgeeks.org", "javatpoint.com", "medium.com"]
    for site in site_searches:
        site_query = f"{topic} site:{site}"
        print(f"Site-specific search: '{site_query}'")
        site_links = search_google(site_query, subject_name, num_results=2)
        if site_links:
            fallback_links.extend(site_links)
            break  # Stop if we get any results

    return fallback_links[:3] if fallback_links else ["No results found"]

# Load syllabus data
def load_syllabus(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Syllabus file '{file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Syllabus file '{file_path}' contains invalid JSON.")
    return None

# Find article links based on syllabus topics
def find_article_links(syllabus_content, subject_name):
    article_links = {}
    for module, topics in syllabus_content.items():
        module_links = {}
        for topic in topics:
            print(f"Searching articles for topic: '{topic}' in module: '{module}'")
            links = search_google(topic, subject_name)
            if not links:  # If no links found, use fallback method
                print(f"No initial results found for '{topic}'. Trying fallback search...")
                links = fallback_search(topic, subject_name)
            module_links[topic] = links[0] if links else "No results found"
        article_links[module] = module_links
    return {"Syllabus_content": article_links}

# Save the results to a JSON file
def save_results(data, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create the directory if it doesn't exist
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Results successfully saved to '{output_file}'")

# Main function
def main():
    syllabus_file = "models/syllabus.json"
    output_file = "models/links/article_links.json"

    # Load syllabus data
    syllabus_data = load_syllabus(syllabus_file)
    if not syllabus_data:
        return

    # Dynamically fetch the first top-level key (subject name)
    subject_name = list(syllabus_data.keys())[0]
    syllabus_content = syllabus_data[subject_name].get("Syllabus_content")

    if not syllabus_content:
        print(f"Error: No syllabus content found for '{subject_name}'.")
        return

    # Clean subject name (handle cases with "and", "&", or other separators)
    subject = subject_name.split('and')[0].strip() if 'and' in subject_name else subject_name
    subject = subject.split('&')[0].strip() if '&' in subject else subject

    # Find article links and save results
    article_links = find_article_links(syllabus_content, subject)
    result_data = {subject_name: article_links}  # Wrap in subject key
    save_results(result_data, output_file)

if __name__ == "__main__":
    main()

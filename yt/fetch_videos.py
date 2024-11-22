import os
import re
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env.local
load_dotenv('models/yt/.env.local')

# Access the API key from environment variables
api_key = os.getenv('API_KEY')
print(api_key)

def iso_to_hms(duration):
    # Regex pattern to extract hours, minutes, and seconds
    pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
    match = re.match(pattern, duration)

    if match:
        # Extract hours, minutes, and seconds or set to 0 if not present
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0

        # Format and return as HH:MM:SS
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return "0:00:00"
    
# Function to fetch YouTube videos for syllabus topics
def fetch_youtube_videos(api_key, syllabus_content, subject_name, max_results=1):
    # Build the YouTube service
    youtube = build('youtube', 'v3', developerKey=api_key)
    subject =""
    if 'and' in subject_name:
        subject = subject_name.split('and')[0].strip()
    elif '&' in subject_name:
        subject = subject_name.split('&')[0].strip()

    # Dictionary to store video details in JSON format
    video_results = {}
    
    # Loop through each module and its topics
    for module, topics in syllabus_content.items():
        video_results[module] = []  # Initialize a list for each module

        # Loop through all topics in the module (topics is a list of strings)
        for topic in topics:
            enhanced_query = f"{topic} in {subject}"  # Create enhanced search query for the topic

            # Make the search request for the enhanced query
            request = youtube.search().list(
                part="snippet",
                q=enhanced_query,  # Search query for each topic
                type="video",  # Only fetch videos
                maxResults=max_results,  # Limit the number of results to 1
                order="relevance"  # Get the most relevant results
            )

            # Execute the request and get the response
            response = request.execute()

            # Extract video details from the response
            for item in response['items']:
                if 'videoId' in item['id']:
                    video_id = item['id']['videoId']
                    # Fetch video details to get the duration
                    video_response = youtube.videos().list(
                        part="contentDetails",
                        id=video_id
                    ).execute()

                    # Extract the video duration (ISO 8601 format)
                    duration = video_response['items'][0]['contentDetails']['duration']
                    video_length = iso_to_hms(duration) 
                    video_details = {
                        'topic': topic,
                        'enhanced_query': enhanced_query,
                        'title': item['snippet']['title'],
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'description': item['snippet']['description'],
                        'duration': video_length  # Add the duration here
                    }
                    video_results[module].append(video_details)
    
    
    return {subject_name: video_results}


# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save JSON data
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
if __name__ == "__main__":
    # Load syllabus data from JSON file
    json_file_path = 'models/yt_test.json'  # Replace with your JSON file path
    data = load_json(json_file_path)

    # Extract the subject name dynamically (the first key in the JSON file)
    subject_name = list(data.keys())[0]  # The first key is the subject name


    # Extract syllabus content under the subject name
    syllabus_content = data.get(subject_name, {}).get('Syllabus_content', {})
    
    # Fetch videos using syllabus content and subject name
    videos = fetch_youtube_videos(api_key, syllabus_content, subject_name)

    # Save the results to a new JSON file
    output_file_path = 'models/yt/youtube_details.json'
    save_json(output_file_path, videos)

    print(f"YouTube video details saved to {output_file_path}")

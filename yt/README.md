
# YouTube Video Fetcher for Syllabus Topics

This project fetches YouTube videos related to syllabus topics, using the YouTube Data API and stores the results in a `youtube_details.json` file. The JSON is reduced in size to avoid exceeding API limits. The API will be queried using enhanced search queries for each syllabus topic.

## Folder Structure

Here is the folder structure for the project:

```
models/
└── yt/
    ├── .env.local
    ├── fetch_videos.py
    └── youtube_details.json
```

- **`.env.local`**: This file contains your YouTube Data API key.
- **`fetch_videos.py`**: This is the Python script that fetches the video details from YouTube.
- **`youtube_details.json`**: The output file where YouTube video details (title, URL, description, and duration) will be saved.

## Installation Instructions


1. **Install the required dependencies**:
   Install the necessary packages using pip:
   ```bash
   pip install google-api-python-client python-dotenv
   ```

2. **Configure your YouTube API key**:
   - Create a `.env.local` file in the `models/yt/` folder.
   - Add your YouTube Data API key to the `.env.local` file in the following format:
     ```
     API_KEY=your_api_key_here
     ```
   - Replace `your_api_key_here` with your actual API key.

3. **Run the script**:
   Once the setup is complete, you can fetch the videos by running the script:
   ```bash
   python fetch_videos.py
   ```

   - This will fetch YouTube videos based on syllabus topics and store the results in `youtube_details.json` inside the `models/yt/` folder.

## Notes

- The YouTube API has a usage limit. To prevent exceeding the daily quota, the code has been designed to minimize API calls by limiting the number of results fetched for each topic.
- The `youtube_details.json` file will contain the following data:
  - `topic`: The topic from the syllabus.
  - `enhanced_query`: The enhanced search query used for fetching YouTube videos.
  - `title`: The title of the YouTube video.
  - `url`: The URL of the YouTube video.
  - `description`: The description of the video.
  - `duration`: The duration of the video in `HMS` format.

## Folder Structure Explained

- **`models/yt/`**:
   - This folder contains the `.env.local` file, Python script, and the output JSON file. The `.env.local` file should be in this folder to ensure proper API access.
   - The output file, `youtube_details.json`, will be automatically created when you run the script.

---

I hope this version is more aligned with your expectations! If you need any more adjustments, let me know.
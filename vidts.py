import streamlit as st
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

load_dotenv()

# Configure YouTube Data API and Gemini API
YOUTUBE_DATA_API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

youtube = build(serviceName='youtube', version='v3', developerKey=YOUTUBE_DATA_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
genai_model = genai.GenerativeModel('gemini-pro')

# Helper functions
def search_yt(query, max_results=2):
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=query,
        videoCaption='closedCaption',
        type='video',
    )
    response = request.execute()
    return response.get("items", [])

def get_transcript(video_id, languages=['en','en-US','en-GB']):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
    transcript = TextFormatter().format_transcript(transcript)
    return transcript

def get_ai_extract(prompt, text):
    response = genai_model.generate_content(prompt + text, stream=False)
    return response.text

def extract_video_id(youtube_link):
    parsed_url = urlparse(youtube_link)
    video_id = parse_qs(parsed_url.query).get('v')
    return video_id[0] if video_id else None

# Streamlit interface
st.title("YouTube Video Notes Extractor")
st.write("Generate notes from YouTube videos by searching a topic or pasting a video link.")

# Initialize session state variables for follow-up questions
if "follow_up_notes" not in st.session_state:
    st.session_state.follow_up_notes = ""
if "follow_up_query" not in st.session_state:
    st.session_state.follow_up_query = ""
if "current_notes" not in st.session_state:
    st.session_state.current_notes = ""
if "current_video_id" not in st.session_state:
    st.session_state.current_video_id = ""

# Tab selection
tab_selection = st.radio("Choose an option:", ("Search by Topic", "Search by Video Link"))

# If user chooses "Search by Topic"
if tab_selection == "Search by Topic":
    query = st.text_input("Enter a topic to search on YouTube:")
    
    if st.button("Search and Generate Notes"):
        if query:
            search_results = search_yt(query, max_results=2)
            if search_results:
                for result in search_results:
                    video_id = result["id"]["videoId"]
                    video_title = result["snippet"]["title"]
                    st.subheader(f"{video_title}")
                    st.video(f"https://www.youtube.com/watch?v={video_id}")
                    
                    transcript = get_transcript(video_id)
                    notes = get_ai_extract("Extract notes: ", transcript)
                    st.write("### Notes:")
                    st.write(notes)
                    
                    # Store current notes and video ID in session state
                    st.session_state.current_notes = notes
                    st.session_state.current_video_id = video_id
                    
            else:
                st.write("No results found.")
        else:
            st.write("Please enter a topic to search.")

# If user chooses "Search by Video Link"
elif tab_selection == "Search by Video Link":
    youtube_link = st.text_input("Enter a YouTube video link:")
    
    if st.button("Generate Notes"):
        video_id = extract_video_id(youtube_link)
        
        if video_id:
            st.session_state.current_video_id = video_id
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            
            transcript = get_transcript(video_id)
            notes = get_ai_extract("Summarize and extract notes: ", transcript)
            st.write("### Notes:")
            st.write(notes)
            
            # Store current notes in session state
            st.session_state.current_notes = notes
            
        else:
            st.write("Invalid YouTube link. Please provide a valid link.")

# Follow-up Query Section
if st.session_state.current_notes:
    follow_up_query = st.text_input("Ask something else about the video", key="follow_up_query_input")
    if st.button("Get Answer", key="follow_up_button"):
        if follow_up_query:
            follow_up_notes = get_ai_extract(follow_up_query + ": ", st.session_state.current_notes)
            st.session_state.follow_up_notes = follow_up_notes  # Store follow-up notes in session state
    
    # Display follow-up answer if available
    if st.session_state.follow_up_notes:
        st.write("### Follow-up Answer:")
        st.write(st.session_state.follow_up_notes)

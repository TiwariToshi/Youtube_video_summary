#makersuite - API Key used here in .env file

#### To Run the code - 
# 1.source env/bin/activate
# 2.python -m streamlit run app.py



import streamlit as st
from dotenv import load_dotenv
#import google as genai
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()  #load the environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

prompt = """You are a Youtube video summarizer .You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words.Please provide the summary of the given context"""

ytt_api = YouTubeTranscriptApi()

## Getting transcript from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text= ytt_api.fetch(video_id)


        transcript=""
        for i in transcript_text:
            transcript += " " + i.text

        return transcript
    except Exception as e:
        raise e
    
##Getting the summary based on the prompt from Google gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt+transcript_text)
    return response.text


st.title("Youtube  Transcript to Detailed Notes Converter")
youtube_link =st.text_input("Enter Youtube video link")

if youtube_link:
    video_id=youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("##Detailed Notes:")
        st.write(summary)


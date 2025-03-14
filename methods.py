from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from googleapiclient.discovery import build
from langchain_ollama import ChatOllama


def URL_to_ID(URL):
    return URL.split("v=")[-1].split("&")[0]

def get_original_language(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Get the first available transcript (original, not translated)
        for transcript in transcripts:
            return transcript.language_code  # Return the language code (e.g., "en", "ur", "hi")

    except NoTranscriptFound:
        return None  # No transcript available
    except TranscriptsDisabled:
        return None  # Transcripts disabled
    except Exception as e:
        return None  # Handle other errors





def get_transcript_vedio(vedio_url):
    video_id = URL_to_ID(vedio_url)
    print(
        get_original_language(video_id)
    )
    
    lan_code=get_original_language(video_id)
    languages=[lan_code]
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=languages)
        return "\n".join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error: {str(e)}"
    


# def get_all_comments(vedio_url):
#     youtube = build("youtube", "v3", developerKey=API_KEY)
    
#     comments = []
#     next_page_token = None
    
#     while True:
#         response = youtube.commentThreads().list(
#             part="snippet",
#             videoId = URL_to_ID(vedio_url),
#             textFormat="plainText",
#             maxResults=100,  # Fetch 100 comments per request
#             pageToken=next_page_token
#         ).execute()
        
#         for item in response["items"]:
#             comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
#             comments.append(comment)
        
#         # Check if there are more pages of comments
#         next_page_token = response.get("nextPageToken")
#         if not next_page_token:
#             break  # Exit loop if no more comments
    
#     return comments



def get_bot_response(content):
    llm = ChatOllama(
        model="deepseek-r1:1.5b",
        # model="llama3.2",
        temperature=0.5,
    )

    messages = [
    (
        "system",
        "You are a helpful assistant that will summarize the given content to one third of original",
    ),
    
    (
        "system",
        "You will just provide summarized content not extra words like 'here is the content' etc.",
    ),
    
    (
        "system",
        "You will make proper headings and bullet points and also agjust spaces and endlines if required",
    ),
    
    ("human", 
     f"summarze this content : {content}"
    ),
    
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

    

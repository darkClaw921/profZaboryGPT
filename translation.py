from openai import OpenAI
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=key,)

def transcript_audio(pathFile:str):
    audio_file = open(pathFile, "rb")
    transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    return transcript
# audio_file = open("1700907333.16811.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file, 
#   response_format="text"
# )
# pprint(transcript)
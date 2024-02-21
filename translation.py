from openai import OpenAI
import os
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()
key = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=key,)

def transcript_audio(pathFile:str):
    print(pathFile)
    print('transcript_audio')
    audio_file = open(pathFile, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text",
        prompt="разбери этот аудиофайл и напиши по строчкам кто горорил Клиент: или Оператор: учитывай что первый говорил Оператор:"
        # prompt="disassemble this audio file and write in the format Client: Operator:"

    )

    return transcript
# audio_file = open("1700907333.16811.mp3", "rb")
# transcript = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file, 
#   response_format="text"
# )
# pprint(transcript)
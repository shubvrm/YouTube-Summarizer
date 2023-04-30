from flask import Flask
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline



# define a variable to hold you app
app = Flask(__name__)

def splitText(text):
    words = text.split(" ") # list of all words
    chunk = ""
    chunks = []

    for i in words:
        chunk += i + " "
        if len(chunk.split(" ")) == 700:
            chunks.append(chunk.strip())
            chunk = ""

    if chunk.strip():
        chunks.append(chunk.strip())

    return chunks


# define your resource endpoints
@app.route('/', methods=['GET'])
def mainfn():

    summarization = pipeline("summarization")

    fullTranscript=""
    fullSummary=""
    text= YouTubeTranscriptApi.get_transcript("ztp81n3xCBs")
    for i in text:
        fullTranscript+= " "+ i["text"]
    
    chunks= splitText(fullTranscript)

    for i in chunks:
        summary_text = summarization(i[:1024])[0]['summary_text']
        fullSummary+=summary_text
    
    return(fullSummary)


    
# server the app when this file is run
if __name__ == '__main__':
    app.run()
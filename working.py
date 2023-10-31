from pytube import YouTube
import requests
#from bardapi.constants import SESSION_HEADERS
#from bardapi import Bard
from youtube_transcript_api import YouTubeTranscriptApi
import re
import nltk 
from nltk.corpus import stopwords 
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize, sent_tokenize 
import google.generativeai as palm
import googletrans
from deep_translator import GoogleTranslator

def translate(text,target):
    #print("HERE")
    #print(str(text),str(target))
    translated = GoogleTranslator(source='auto', target=str(target)).translate(text=str(text))
    # Print the translated text
    return translated


#from bing-chat import BingChat
def connect_to_palm(context,messages):
    palm.configure(api_key="AIzaSyDfMzRm8ehgo9qz5CaCn1PzCGHs4M1OuyM")

    defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    }

    examples = []
    #messages.append("NEXT REQUEST")
    context= context+"\n Answer the question based on above context provided"
    response = palm.chat(
    **defaults,
    context=context,
    examples=examples,
    messages=messages
    )

    return response.last


def connect_to_bard():
    token = "bwgU8TveH-GFFV_RB3apyRqLtegfK5V6ZcMuNaj8kLnku-SjCGSK-dlH-cEHRIu7BoOmxw."
    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", token)
    session.cookies.set("__Secure-1PSIDTS", "sidts-CjEBNiGH7oqlz_hYccC4NlZnYb7M20MMQuHNt--2yuVXvaEyhCQdC9RFC0U-pIwC0_ttEAA")
    session.cookies.set("__Secure-1PSIDCC", "ACA-OxNKSFA1dG7piN4E7u2bLV3VqnGhHL4D5ec-5gKEZf0Ix_LxkDnorESGlxDIVfdKu13xmeg")
    bard = Bard(token=token, session=session)
    return bard

def get_text_from_url(url):
    # Regular expression pattern to match the video ID
    pattern = r"v=([A-Za-z0-9_-]+)"

    # Search for the pattern in the URL
    match = re.search(pattern, url)

    if match:
        video_id = match.group(1)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        joined_text = ' '.join(entry['text'] for entry in transcript)
    except Exception as e:
        print("An error occurred:", str(e))
        return False
    return joined_text


def text_summary(joined_text):
    # Input text - to summarize  
    text = joined_text

    # Tokenizing the text 
    stopWords = set(stopwords.words("english")) 
    words = word_tokenize(text) 

    # Creating a frequency table to keep the  
    # score of each word 

    freqTable = dict() 
    for word in words: 
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1

    # Creating a dictionary to keep the score 
    # of each sentence 
    sentences = sent_tokenize(text) 
    sentenceValue = dict() 

    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq 



    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 

    # Average value of a sentence from the original text 

    average = int(sumValues / len(sentenceValue)) 

    # Storing sentences into our summary. 
    summary = '' 
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.3 * average)): 
            summary += " " + sentence 
    return summary

def generate_answer(bard,summary,question):
    res = bard.get_answer(f"{summary} \n {question}")
    print(res['content'])
    return str(res['content'])

def startcode():
    url= input("Enter url: ")
    if url :
        text= get_text_from_url(url)
        if text:
            summary=text_summary(text)
            while True:
                ques = input("\nEnter question or enter gg to end: ")
                print("\n")
                if ques != 'gg':
                    generate_answer(text,ques)
                    print("\n")
                else:
                    break
        else:
            print("Some Error in text generation") 
    else:
        print("error in url")   


def connect_to_bing():
    logging.basicConfig(level=logging.INFO)
    chat = BingChat("")
    initial_message = "Hello, Bing!"
    messages = chat.run(initial_message)
    print("Chat history:", messages)

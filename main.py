from pydoc import text

import speech_recognition as sr 
import webbrowser            # a built in module to open the web browser
import pyttsx3
import musicLibrary
import requests
from google import genai
from dotenv import load_dotenv
load_dotenv()


recognizer = sr.Recognizer() #helper to recognize the speech of the user
engine = pyttsx3.init()      #helper to speak the text 
newsapi = "<Your Key Here>"


def speak(text):
    engine.say(text)         #to make the engine say the text 
    engine.runAndWait()      #to make the engine wait until it finishes saying the text


import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def aiProcess(text):
    print("text received for AI processing:", text)
    response = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=f"""
                You are Jarvis, a voice-based AI assistant.

                Rules:
                - Keep responses short (1-2 lines max)
                - Be fast and direct
                - No extra explanations

                User: {text}
                """
                    )

    return response.text 




def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open twitter" in c.lower():
        webbrowser.open("https://www.twitter.com")
    elif c.lower().startswith("play"):
        song = " ".join(c.lower().split(" ")[1:])
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # Let GEMINI handle the request
        output = aiProcess(c)
        print("AI OUTPUT:", output)
        speak(output) 



if __name__ == "__main__":
    speak("Initializing Jarvis...")

    r = sr.Recognizer()
    r.energy_threshold = 300  # improves mic sensitivity

    while True:
        try:
            print("Listening for wake word...")

            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5, phrase_time_limit=3)

            word = r.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                speak("Yes")
                print("Wake word detected")

                with sr.Microphone() as source:
                    print("Jarvis Active...")

                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)

                    print("Command:", command)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio")

        except sr.WaitTimeoutError:
            print("Listening timeout")

        except sr.RequestError as e:
            print("Speech API error:", e)

        except Exception as e:
            print("Error:", e)
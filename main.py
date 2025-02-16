import speech_recognition as sr
import os
import webbrowser
import datetime
import re
import time
import pyttsx3
from transformers import pipeline
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import pyautogui

music_folder = "C:\\Users\\CHANDRAKALA.K\\Musica"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking speed


#initializing the chatbot used to fetch the data in BASIC query
model_name = "facebook/blenderbot-400M-distill"
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
chatbot = pipeline("text-generation", model="facebook/blenderbot-400M-distill")
chatStr = ""


def say(text):
    """Function for text-to-speech output on Windows"""
    engine.say(text)
    engine.runAndWait()


def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"User: {query}\nJarvis: "
    response = chatbot(query, max_length=200, do_sample=True)[0]['generated_text']
    response_text = response.strip()
    say(response_text)
    chatStr += f"{response_text}\n"
    return response_text


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Check your internet connection.")
        return ""

def set_timer(seconds):
    print(f"Timer set for {seconds} seconds...")
    time.sleep(seconds)  # Wait for the timer
    pyautogui.alert("Time's up!", "Timer Alert")  # Show an alert box

def play_song(song_name):
    """Plays a specific song from the music folder."""
    song_path = os.path.join(music_folder, f"{song_name}.mp3")  # Assuming all songs are .mp3
    if os.path.exists(song_path):
        os.system(f'start "" "{song_path}"')
        say(f"Playing {song_name}")
    else:
        say(f"Sorry, I couldn't find {song_name}")

from transformers import pipeline

def take_screenshot():
    """Takes a screenshot and saves it with a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")

def open_maps(destination):
    base_url = "https://www.google.com/maps/dir/?api=1&destination="
    search_url = base_url + destination.replace(" ", "+")  # Format for URL
    webbrowser.open(search_url)


if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    say("Jarvis AI")

    while True:
        query = takeCommand().lower()

        sites = {"youtube": "https://www.youtube.com", "wikipedia": "https://www.wikipedia.org",
                 "google": "https://www.google.com", "mail": "https://www.gmail.com", }
        for site in sites:
            if f"open {site}" in query:
                say(f"Opening {site} my love")
                webbrowser.open(sites[site])
                break

        # Get current time
        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"the time is {hour} hours and {minute} minutes")

        elif "screenshot" in query.lower():
            take_screenshot()

        elif "play" in query and "song" in query:
            song_name = re.sub(r'play( the| my| a)? song ', '', query).strip()
            play_song(song_name)

        elif "navigate to" in query:
            destination = query.replace("navigate to", "").strip()
            say(f"Navigating to {destination}")
            open_maps(destination)

        elif "set timer" in query:
            timei = int(query.replace("set timer","").strip(' for seconds'))
            say(time)
            set_timer(timei)


        elif "code blue" in query.lower():
            say("code blue activated")
            webbrowser.open("https://www.youtube.com/shorts/jMgLPQljdPc")
            while(1):
                query = takeCommand()
                if "up" in query or "slow" in query:
                    pyautogui.scroll(500)
                elif "down" in query or "next" in query:
                    pyautogui.scroll(-500)
                elif "exit" in query or "stop" in query:
                    say("quitting code blue.")
                    break

        elif "code yellow" in query:
            say("Code Yellow activated.")
            os.system("notepad.exe")
            time.sleep(2)

            while True:
                query = takeCommand()

                # Stop condition
                if "break" in query or "enough" in query or "stop" in query or "exit" in query:
                    say("Quitting Code Yellow")
                    break
                elif query:
                    pyautogui.write(query + " ", interval=0.05)  # Type spoken words

        # Exit program
        elif "jarvis quit" in query:
            say("Goodbye, quitting now")
            break

        # Reset chat history
        elif "reset chat" in query:
            chatStr = ""
            say("Chat history reset")

        else:
            chat(query)

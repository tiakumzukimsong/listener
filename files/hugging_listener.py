import os
import speech_recognition as sr
import pyttsx3
import subprocess
from transformers import pipeline

recognizer = sr.Recognizer()
engine = pyttsx3.init()
microphone = sr.Microphone(device_index=3)

voices = engine.getProperty('voices')

for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

generator = pipeline('text-generation', model='gpt2')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def huggingface_response(command):
    try:
        result = generator(command, max_length=1000, num_return_sequences=1)
        reply = result[0]['generated_text'].strip()
        return reply
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't fetch a response."

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Request error. Please check your internet connection.")
            return None

def execute_command(command):
    if "open folder" in command:
        folder_path = "/home/tia/pro"
        subprocess.run(["xdg-open", folder_path])
        speak("Opening folder")

    elif "google" in command:
        application_path = "/usr/bin/google-chrome"
        subprocess.run([application_path])
        speak("Opening Google")

    else:
        response = huggingface_response(command)
        print(f"Response: {response}")
        speak(response)

if __name__ == "__main__":
    speak("How can I assist you?")

    while True:
        command = listen()
        if command:
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            else:
                execute_command(command)

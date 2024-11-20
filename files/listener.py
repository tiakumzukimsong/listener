import os
import speech_recognition as sr
import pyttsx3
import subprocess
import openai



recognizer = sr.Recognizer()
engine = pyttsx3.init()
microphone = sr.Microphone(device_index=3)
    
# print(sr.Microphone.list_microphone_names())


def speak(text):
    engine.say(text)
    engine.runAndWait()


def chatgpt_response(command):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  
            prompt=command,
            max_tokens=100  
        )
        reply = response.choices[0].text.strip()
        return reply
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return "Sorry, I couldn't fetch a response."


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            speak(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("Request error. Please check your internet connection.")
            return None

def execute_command(command):
    if "open folder" in command:
        folder_path = "/home/tia/pro"
        subprocess.run(["xdg-open", folder_path])
        speak("Opening folder")

    # elif "google" in command:
    #     file_path = "/usr/bin/google-chrome"
    #     subprocess.run(["xdg-open", file_path])
    #     speak("Opening file")

    elif "google" in command:
        application_path = "/usr/bin/google-chrome"
        subprocess.run([application_path])
        speak("Opening google")

    # else:
    #     speak("Command not recognized")

    else:
        chatgpt_response(command)

# Main loop
if __name__ == "__main__":
    speak("How can I assist you?")


    while True:
        command = listen()
        print(command)
        if command:
            if "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            else:
                execute_command(command)

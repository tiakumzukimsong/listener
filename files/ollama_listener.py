import os
import speech_recognition as sr
import pyttsx3
import subprocess

recognizer = sr.Recognizer()
engine = pyttsx3.init()
microphone = sr.Microphone(device_index=3)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone(device_index=3) as source:
        recognizer.adjust_for_ambient_noise(source)  
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
            print("Request error. Please check your internet connection.")
            return None

def ollama_response(command):
    try:
        # Call Ollama using subprocess and capture the response
        result = subprocess.run(['ollama', 'run', 'llama2:latest', command], capture_output=True, text=True)

        if result.returncode == 0:
            response = result.stdout.strip()  
            return response
        else:
            return "Sorry, I couldn't fetch a response from Ollama."
    except Exception as e:
        print(f"Error executing Ollama command: {e}")
        return "Sorry, I couldn't fetch a response from Ollama."

def execute_command(command):
    if "open folder" in command:
        folder_path = "/home/tia/pro"
        subprocess.run(["xdg-open", folder_path])
        speak("Opening folder")

    elif "open file" in command:
        file_path = "/path/to/your/file"
        subprocess.run(["xdg-open", file_path])
        speak("Opening file")

    elif "open application" in command:
        application_path = "/path/to/your/application"
        subprocess.run([application_path])
        speak("Opening application")

    else:
        response = ollama_response(command)
        speak(response)

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

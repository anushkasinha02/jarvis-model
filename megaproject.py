import datetime
import webbrowser
import sys

import pyttsx3
import speech_recognition as sr


def speak(text: str) -> None:
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, phrase_time_limit=5)

    try:
        command = recognizer.recognize_google(audio)
        print(f"Heard: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        print("Speech service is unavailable.")
        speak("Speech service is unavailable.")
        return ""


def process_command(command: str) -> bool:
    if not command:
        return True

    if "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye. Have a nice day.")
        return False

    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        return True

    if "open browser" in command or "open google" in command:
        speak("Opening your browser.")
        webbrowser.open("https://www.google.com")
        return True

    if "search for" in command:
        query = command.split("search for", 1)[1].strip()
        if query:
            speak(f"Searching for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("Please tell me what to search for.")
        return True

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you today?")
        return True

    speak(f"You said: {command}")
    return True


def main() -> None:
    speak("Hello, I am your virtual assistant. Say something when you are ready.")
    print("Virtual AI assistant is ready. Say 'exit' to quit.")

    running = True
    while running:
        command = listen()
        running = process_command(command)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        speak("Shutting down. Goodbye.")
        sys.exit(0)

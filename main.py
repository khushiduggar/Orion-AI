import openai
import speech_recognition as sr
import pyttsx3
import webbrowser

# Set up your OpenAI API key
openai.api_key = 'sk-proj-gYswxgOJj-----(add your own open api key)'

# Text-to-speech function
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Speech recognition function
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        query = ""
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        query = ""

    return query.lower()

# Function to interact with OpenAI using GPT-3.5-turbo
def openai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Updated to the latest model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        return f"An error occurred: {e}"

# Function to generate a resignation email
def generate_resignation_email():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write an email to my boss for resignation?"}
        ]
    )
    
    email_text = response.choices[0].message['content'].strip()
    return email_text

# Command processor
def process_command(command):
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")
    elif "open wikipedia" in command:
        webbrowser.open("https://www.wikipedia.com")
        speak("Opening Wikipedia")
    elif "generate resignation email" in command:
        resignation_email = generate_resignation_email()
        speak("Here is your resignation email.")
        print(resignation_email)  # Print the email to the console
    elif "exit" in command:
        speak("Goodbye!")
        return False
    else:
        # Use OpenAI for other queries
        answer = openai_response(command)
        speak(answer)
    return True

# Main function
if __name__ == "__main__":
    speak("Hello, I am Orion AI. How can I assist you today?")

    while True:
        command = listen()
        if command:
            if not process_command(command):
                break
        else:
            speak("Sorry, I did not catch that. Could you please repeat?")

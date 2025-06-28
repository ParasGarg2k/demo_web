import pyttsx3

def save_text_to_speech(text, filename='output.wav'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    engine.save_to_file(text, filename)  # Save speech to a WAV file
    engine.runAndWait()
    print(f"Audio saved to {filename}")

if __name__ == "__main__":
    user_input = input("Enter text to convert to speech and save: ")
    save_text_to_speech(user_input)

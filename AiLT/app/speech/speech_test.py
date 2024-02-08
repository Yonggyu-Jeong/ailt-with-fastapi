import speech_recognition as sr

def single_threaded_recognition():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            print("Start speaking...")
            audio_data = recognizer.listen(source, timeout=5)  # Timeout 설정 (5초)

        try:
            text = recognizer.recognize_google(audio_data)
            print("Recognized Text:", text)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    except KeyboardInterrupt:
        print("Recognition process interrupted by user.")

if __name__ == "__main__":
    single_threaded_recognition()

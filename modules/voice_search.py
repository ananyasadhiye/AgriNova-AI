import speech_recognition as sr

def listen_crop():

    r = sr.Recognizer()

    try:
        with sr.Microphone(device_index=1) as source:   # IMPORTANT CHANGE
            print("Listening... Speak now")

            r.adjust_for_ambient_noise(source, duration=1)

            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        text = r.recognize_google(audio)

        print("You said:", text)

        return text.lower()

    except sr.UnknownValueError:
        return "could not understand audio"

    except sr.RequestError as e:
        return f"speech service error {e}"

    except Exception as e:
        return f"microphone error {e}"
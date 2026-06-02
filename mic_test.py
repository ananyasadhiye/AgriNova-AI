import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone(device_index=9) as source:
    print("Speak now...")
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio)
    print("You said:", text)

except sr.UnknownValueError:
    print("Google could not understand audio")

except sr.RequestError as e:
    print("API error:", e)
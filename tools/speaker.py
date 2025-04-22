import pyttsx3

def falar(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('voice', 'brazil')
    engine.say(texto)
    engine.runAndWait()
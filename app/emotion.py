from textblob import TextBlob

def detect_emotion(text:str) -> str:
    pol = TextBlob(text).sentiment.polarity
    if pol < -0.2: return "frustrado"
    if pol >  0.2: return "positivo"
    return "neutral"

def empathetic_prefix(emotion:str) -> str:
    if emotion == "frustrado":
        return "Lamento la dificultad; voy a revisar la documentación para ayudarte rápido. "
    return ""
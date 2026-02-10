from gtts import gTTS

for i in range(65, 91):
    letter = chr(i)
    tts = gTTS(text=letter, lang='en')
    tts.save(f"{letter}.mp3")
    print(f"Saved {letter}.mp3")

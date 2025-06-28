from gtts import gTTS
import os

text = input("Please Enter sentences to save to an input file")
output = gTTS(text=text, lang='en', slow=False)
output.save('output.mp3')

os.system("start output.mp3")
import pyttsx3


class TextToSpeechEngine:

    def __init__(self):
        self.engine = None
        try:
            self.engine = pyttsx3.init()
            # Optional: Set properties like rate, volume, or voice
            self._engine.setProperty('rate', 150)  # Speed of speech
            self._engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
            voices = self._engine.getProperty('voices')
            if voices:
                self._engine.setProperty('voice', voices[0].id)  # Try to set first available voice

        except Exception as e:
            print(f"error initializing pyttsx3 : {e}")


    def is_ready(self):
        return self.engine is not None

    def speak(self,text):
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            raise RuntimeError("Text-to-Speech engine is not initialized.")
    def stop(self):
        self.engine.stop()

    def get_voices(self, voice_id):
        if self._engine:
            return self._engine.getProperty('voices')
        return []
    def set_voices(self, voice_id):
        if self._engine:
            self._engine.setProperty('voice', voice_id)

    def set_rate(self, rate):
        """
        Sets the speech rate.
        """
        if self._engine:
            self._engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """
        Sets the speech volume.
        """
        if self._engine:
            self._engine.setProperty('volume', volume)
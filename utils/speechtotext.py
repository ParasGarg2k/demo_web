import whisper
import numpy as np
import soundfile as sf

class SpeechToText:
    def __init__(self, model_size='small'):
        """
        Initialize Whisper speech recognition model.
        model_size: one of ['tiny', 'base', 'small', 'medium', 'large']
        """
        print(f"Loading Whisper model ({model_size})...")
        self.model = whisper.load_model(model_size)

    def transcribe_audio(self, audio_path):
        """
        Transcribe an audio file to text.
        Args:
            audio_path (str): path to audio file (.wav, .mp3, etc)
        Returns:
            str: recognized text
        """
        # Load audio and pad/trim it to fit 30 seconds context window
        audio, sr = sf.read(audio_path)
        if sr != 16000:
            # Resample if needed
            import resampy
            audio = resampy.resample(audio, sr, 16000)
            sr = 16000

        # Whisper expects float32 np array, mono
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        audio = audio.astype(np.float32)

        result = self.model.transcribe(audio, language='en')
        return result['text']

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python speech_to_text.py <audio_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    stt = SpeechToText(model_size='small')
    text = stt.transcribe_audio(audio_file)
    print(f"Transcribed Text:\n{text}")

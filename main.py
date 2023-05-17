import io
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
from flask import Flask, request, jsonify

app = Flask(__name__)





@app.route('/upload', methods=['POST'])
def upload_file():

    file = request.files['file']


    # Read audio data from the byte array
    audio_data = file.read()

    # Convert audio to WAV format
    wav_data, sample_rate = convert_to_wav(audio_data)

    if wav_data is None:
        return jsonify({'error': 'unsupported audio format'}), 400

    # Convert audio to text
    text = transcribe_audio(wav_data, sample_rate)

    return jsonify({'transcript': text})


def convert_to_wav(audio_data):
    """Convert the audio data to WAV format."""
    try:
        # Convert byte data to float array
        float_data = np.frombuffer(audio_data, dtype=np.float32)

        # Convert to int16 array (16-bit PCM)
        int_data = np.int16(float_data * np.iinfo(np.int16).max)

        # Save as WAV file
        wav_path = r"C:\Users\user\PycharmProjects\pythonProject\audiostemp.wav"
        write(wav_path, 44100, int_data)

        # Read the converted WAV file
        with open(wav_path, "rb") as wav_file:
            wav_data = wav_file.read()

        return wav_data, 44100

    except Exception as e:
        print("Error during audio conversion:", str(e))
        return None, None


def transcribe_audio(audio_data, sample_rate):
    """Transcribe the given audio data."""
    r = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(audio_data)) as source:
            audio = r.record(source)
            text = r.recognize_sphinx(audio, show_all=False, language='en-US', keyword_entries=None, grammar=None)
            return text

    except sr.UnknownValueError:
        return jsonify({'error': 'Unable to transcribe audio'})
    except sr.RequestError as e:
        return jsonify({'error': 'Error during audio transcription', 'details': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

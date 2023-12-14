# Run this in the consol first :

# pip install sounddevice numpy scipy pydub keyboard

# Don't forget to install whisper


import whisper


import sounddevice as sd

import numpy as np

import scipy.io.wavfile as wav

from pydub import AudioSegment

from dora import Node

import time

import pyarrow as pa

node = Node()


# Set the parameters for recording

fs = 44100  # sample rate

max_duration = 30

audio_data = []

model = whisper.load_model("base")

recorded = False

stop = False
import time


def start_recording():
    print("Recording... Press SPACE to stop.")

    global audio_data

    audio_data = sd.rec(
        int(fs * max_duration),
        samplerate=fs,
        channels=2,
        dtype=np.int16,
        blocking=False,
    )


def stop_recording():
    sd.stop()
    wav_file_path = "recorded_audio.wav"

    wav.write(wav_file_path, fs, audio_data)


def run():
    # audio_data = whisper.pad_or_trim(audio_data)

    wav_file_path = "recorded_audio.wav"

    wav.write(wav_file_path, fs, audio_data)

    # Convert the WAV file to MP3

    mp3_file_path = "recorded_audio.mp3"

    audio = AudioSegment.from_wav(wav_file_path)

    audio.export(mp3_file_path, format="mp3")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(mp3_file_path)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # # detect the spoken language
    # _, probs = model.detect_language(mel)
    # print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(language="da")
    result = whisper.decode(model, mel, options)

    print(result.text)


for event in node:
    if event["type"] == "INPUT":
        start_recording()

        time.sleep(5)

        stop_recording()
        node.send_output("path", pa.array(["recorded_audio.wav"]))

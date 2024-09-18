import os
import whisper
import pysrt
from pydub import AudioSegment

# Load Whisper model
model = whisper.load_model("base")

# Paths
input_audio = 'ExtractedFiles/audio.mp3'
srt_file = 'ExtractedFiles/audio.srt'
censor_words_file = 'CensoredDictionary.txt'
output_audio = 'ExtractedFiles/censored_audio.mp3'

# Step 1: Transcribe the audio file using Whisper and save SRT
def transcribe_audio_to_srt(audio_file_path, model, srt_file_path):
    result = model.transcribe(audio_file_path)
    segments = result['segments']
    
    # Save transcription to SRT file
    with open(srt_file_path, 'w') as srt_file:
        for i, segment in enumerate(segments):
            start = segment['start']
            end = segment['end']
            text = segment['text']
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{format_time(start)} --> {format_time(end)}\n")
            srt_file.write(f"{text}\n\n")

# Helper function to format time for SRT file
def format_time(seconds):
    millisec = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins = (seconds // 60) % 60
    secs = seconds % 60
    hours = seconds // 3600
    return f"{hours:02}:{mins:02}:{secs:02},{millisec:03}"

# Step 2: Load the censor words dictionary
def load_censor_words(censor_words_file):
    with open(censor_words_file, 'r') as file:
        censor_words = [line.strip().lower() for line in file.readlines()]
    return censor_words

# Step 3: Find segments to censor
def find_censor_segments(subs, censor_words):
    censor_segments = []
    for sub in subs:
        start = sub.start.ordinal / 1000.0  # Convert to seconds
        words = sub.text.split()
        for i, word in enumerate(words):
            clean_word = ''.join(e for e in word if e.isalnum()).lower()  # Remove punctuation and lowercase
            if clean_word in censor_words:
                word_start = start + (i / len(words)) * (sub.end.ordinal / 1000.0 - start)  # Estimate word position
                word_end = start + ((i + 1) / len(words)) * (sub.end.ordinal / 1000.0 - start)
                censor_segments.append((word_start, word_end))
    return censor_segments

# Step 4: Mute segments in audio
def mute_audio_segments(audio_file_path, censor_segments, output_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    for start, end in censor_segments:
        start_ms = start * 1000  # Convert to milliseconds
        end_ms = end * 1000  # Convert to milliseconds
        silence = AudioSegment.silent(duration=end_ms - start_ms)
        audio = audio[:start_ms] + silence + audio[end_ms:]
    audio.export(output_file_path, format="mp3")

# Transcribe the audio file to SRT
transcribe_audio_to_srt(input_audio, model, srt_file)

# Load SRT file
subs = pysrt.open(srt_file)

# Load censor words
censor_words = load_censor_words(censor_words_file)

# Find segments to censor
censor_segments = find_censor_segments(subs, censor_words)

# Mute segments in audio and save the output
mute_audio_segments(input_audio, censor_segments, output_audio)

print("Censored audio saved to:", output_audio)

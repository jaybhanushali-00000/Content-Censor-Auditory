import os
import pysrt
from pydub import AudioSegment

# Paths
input_audio = 'ExtractedFiles/audio.mp3'
srt_file = 'ExtractedFiles/audio.srt'
censor_words_file = '../../uploads/CensoredDictionary.txt'
output_audio = 'ExtractedFiles/censored_audio.mp3'

# Step 1: Load the censor words dictionary
def load_censor_words(censor_words_file):
    with open(censor_words_file, 'r') as file:
        censor_words = [line.strip().lower() for line in file.readlines()]
    return censor_words

# Step 2: Find segments to censor from the provided SRT file
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

# Step 3: Mute segments in audio
def mute_audio_segments(audio_file_path, censor_segments, output_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    for start, end in censor_segments:
        start_ms = start * 1000  # Convert to milliseconds
        end_ms = end * 1000  # Convert to milliseconds
        silence = AudioSegment.silent(duration=end_ms - start_ms)
        audio = audio[:start_ms] + silence + audio[end_ms:]
    audio.export(output_file_path, format="mp3")

# Load SRT file
subs = pysrt.open(srt_file)

# Load censor words
censor_words = load_censor_words(censor_words_file)

# Find segments to censor
censor_segments = find_censor_segments(subs, censor_words)

# Mute segments in audio and save the output
mute_audio_segments(input_audio, censor_segments, output_audio)

print("Censored audio saved to:", output_audio)

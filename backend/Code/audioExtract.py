#brew install ffmpeg
#pip install ffmpeg-python

import ffmpeg

input_file = '../../uploads/input.mp4'
audio_output = 'ExtractedFiles/audio.mp3'
video_output = 'ExtractedFiles/video.mp4'

#Extracting Audio
ffmpeg.input(input_file).output(audio_output,acodec='mp3').run()

#Extracting Video
ffmpeg.input(input_file).output(video_output,codec='copy',an=None).run()

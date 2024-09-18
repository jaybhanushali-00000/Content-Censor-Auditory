import ffmpeg

def stitch_audio_video(audio_file, video_file, output_file):
    input_video = ffmpeg.input(video_file)
    input_audio = ffmpeg.input(audio_file)

    # Use ffmpeg.filter to combine streams and specify maps using setpts filter
    ffmpeg.output(
        input_video,
        input_audio,
        output_file,
        vcodec='copy',       # Copy the video codec
        acodec='aac'         # Encode audio as AAC
    ).global_args(
        '-map', '0:v',       # Map video stream from the first input
        '-map', '1:a'        # Map audio stream from the second input
    ).run(overwrite_output=True)

audio_file = 'ExtractedFiles/censored_audio.mp3'
video_file = 'ExtractedFiles/video.mp4'
output_file = '../OUTPUT_DIR/Final_video.mp4'

stitch_audio_video(audio_file, video_file, output_file)

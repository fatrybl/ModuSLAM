from pathlib import Path

from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

current_dir = Path(__file__).parent.absolute()
imgs_dir = current_dir / "images"
audio_dir = current_dir / "audio"

image_files = [
    "iros2025-01.png",
    "iros2025-02.png",
    "iros2025-03.png",
    "iros2025-04.png",
    "iros2025-05.png",
    "iros2025-06.png",
    "iros2025-07.png",
    "iros2025-08.png",
    "iros2025-09.png",
    "iros2025-10.png",
    "iros2025-11.png",
    "iros2025-12.png",
]  # Add more images as needed
audio_files = [
    "1.wav",
    "2.wav",
    "3.wav",
    "4.wav",
    "5.wav",
    "6.wav",
    "7.wav",
    "8.wav",
    "9.wav",
    "10.wav",
    "11.wav",
    "12.wav",
]  # Add more audio files as needed

clips = []
for image, audio in zip(image_files, audio_files):
    # Create an ImageClip
    image_path = (imgs_dir / image).absolute()
    audio_path = (audio_dir / audio).absolute()

    image_clip = ImageClip(str(image_path))

    # Load the corresponding audio and get its duration
    audio_clip = AudioFileClip(str(audio_path))
    duration = audio_clip.duration

    # Set the duration of the image clip to match the audio duration
    image_clip = image_clip.with_duration(duration)

    # Set the audio for the image clip
    image_clip = image_clip.with_audio(audio_clip)

    # Add the clip to the list
    clips.append(image_clip)

# Concatenate all clips into a single video
final_video = concatenate_videoclips(clips, method="compose")

# Write the result to a video file with optimizations
result = current_dir / "video.mp4"
final_video.write_videofile(
    str(result),
    fps=12,  # Adjust fps as needed
    codec="libx264",
    preset="ultrafast",  # Use a faster preset
    threads=4,  # Use multiple threads for faster rendering
    bitrate="1000k",
)

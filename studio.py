# create a slideshow from images and videos in a directory

import os
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips
import modules
import effects


def studio(file_path, audio_path):
    modules.Duplicates(file_path).remove()
    # convert videos to .mp4
    modules.convert_videos(file_path)

    tempo, beats = modules.analyze_audio(audio_path)
    images = []
    videos = []
    
    for file in os.listdir(file_path):
        if file.endswith(".jpg"):
            images.append(os.path.join(file_path, file))
        elif file.endswith(".mp4"):
            videos.append(os.path.join(file_path, file))
    # sort after time of creation
    images.sort(key=lambda x: modules.get_metadata(x))
    videos.sort(key=lambda x: modules.get_metadata(x))
    timeline = []
    for image in images:
        timeline.append(ImageClip(image, duration=tempo))
    for video in videos:
        timeline.append(VideoFileClip(video))
    # insert the title clip at the beginning of the timeline
    timeline.insert(0, effects.title("My Slideshow"))
    # render the timeline
    clip = concatenate_videoclips(timeline, method='compose')
    # add audio to the clip
    clip = clip.set_audio(AudioFileClip(audio_path))
    clip.write_videofile("slideshow.mp4")


studio("C:/Users/valen/Downloads/Test",
       "C:/Users/valen/Downloads/Test/audio.wav")

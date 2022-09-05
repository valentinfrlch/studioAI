# create a slideshow from images and videos in a directory

import os
import modules
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips


def studio(path):
    modules.Duplicates(path).remove()
    # convert videos to .mp4
    modules.convert_videos(path)
    images = []
    videos = []
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            images.append(os.path.join(path, file))
        elif file.endswith(".mp4"):
            videos.append(os.path.join(path, file))
    # sort after time of creation
    images.sort(key=lambda x: modules.get_metadata(x))
    print(len(images), len(videos))
    videos.sort(key=lambda x: modules.get_metadata(x))
    timeline = []
    for image in images:
        timeline.append(ImageClip(image, duration=3))
    for video in videos:
        timeline.append(VideoFileClip(video))
    # render the timeline
    clip = concatenate_videoclips(timeline)
    clip.write_videofile("slideshow.mp4", fps=24,
                         codec="libx264", audio_codec="aac")


studio("C:/Users/valen/Downloads/Test")

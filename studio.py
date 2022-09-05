# create a slideshow from images and videos in a directory

import os
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
import modules
import effects


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
    videos.sort(key=lambda x: modules.get_metadata(x))
    timeline = []
    for image in images:
        timeline.append(ImageClip(image, duration=3))
    for video in videos:
        timeline.append(VideoFileClip(video))
    # insert the title clip at the beginning of the timeline
    timeline.insert(0, effects.title("My Slideshow"))
    # render the timeline
    clip = concatenate_videoclips(timeline, method='compose')
    clip.write_videofile("slideshow.mp4")


studio("C:/Users/valen/Downloads/Test")

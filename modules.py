# look for images in directory and check for duplicates
from sys import path_hooks
import imagehash
from PIL import Image
import os
from moviepy.editor import VideoFileClip
import librosa


def get_images(path):
    """Get images from directory"""
    images = []
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            images.append(os.path.join(path, file))
    return images


def get_hash(image):
    """Get hash of image"""
    hash = imagehash.average_hash(Image.open(image))
    return hash


def get_duplicates(images):
    """Get duplicates from images"""
    duplicates = {}
    for image in images:
        hash = get_hash(image)
        if hash not in duplicates:
            duplicates[hash] = []
        duplicates[hash].append(image)
    return duplicates


def remove_duplicates(duplicates):
    """Remove duplicates from images"""
    for hash, images in duplicates.items():
        if len(images) > 1:
            for image in images[1:]:
                os.remove(image)


# create a class to remove duplicates
class Duplicates:
    def __init__(self, path):
        self.path = path
        self.images = get_images(path)
        self.duplicates = get_duplicates(self.images)

    def remove(self):
        remove_duplicates(self.duplicates)


# -----------------------------------------------
# Metadata helper functions
# -----------------------------------------------
def get_metadata(path):
    # get when the image was taken
    time = os.path.getmtime(path)
    return time


# -----------------------------------------------
# File type helper functions
# -----------------------------------------------
# convert videos to .mp4


def convert_videos(path):
    for file in os.listdir(path):
        if file.endswith(".MOV"):
            ori = os.path.join(path, file).replace("\\", "/")
            new = os.path.join(path, file[:-4] + ".mp4").replace("\\", "/")

            # convert video to .mp4 with moviepy
            clip = VideoFileClip(ori)
            clip.write_videofile(new, fps=24,
                                 codec="libx264", audio_codec="aac")
            # remove original video
            os.remove(ori)


# -----------------------------------------------
# Audio helper functions
# -----------------------------------------------

def analyze_audio(path):
    # convert mp3 to wav
    if not path.endswith(".wav"):
        ori = path.replace("\\", "/")
        path = path[:-4] + ".wav"
        ffmpeg_path = "C:/ffmpeg/bin/ffmpeg.exe"
        os.system(ffmpeg_path + ' -i "' + ori + '" "' + path + '"')
    # use librosa to analyze audio
    y, sr = librosa.load(path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    # convert BPM to seconds
    tempo = 60 / tempo
    return tempo, beats

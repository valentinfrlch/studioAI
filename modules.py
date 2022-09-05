# look for images in directory and check for duplicates
import imagehash
from PIL import Image
import os
import subprocess


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


#create a class to remove duplicates
class Duplicates:
    def __init__(self, path):
        self.path = path
        self.images = get_images(path)
        self.duplicates = get_duplicates(self.images)

    def remove(self):
        remove_duplicates(self.duplicates)


#-----------------------------------------------
# Metadata helper functions
#-----------------------------------------------
def get_metadata(path):
    # get when the image was taken
    time = os.path.getmtime(path)
    return time

#-----------------------------------------------
# File type helper functions
#-----------------------------------------------
# convert videos to .mp4


def convert_videos(path):
    for file in os.listdir(path):
        if not path.endswith(".mp4"):
            #check if file is a video
            if subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                            os.path.join(path, file)], stdout=subprocess.PIPE):
                file_path = os.path.join(path, file)
                subprocess.call(
                    ["ffmpeg", "-i", file_path, file_path[:-4] + ".mp4"])
                os.remove(file_path)
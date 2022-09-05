import numpy as np

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

def title(title, duration=3, color='white', fontsize=70, font='Amiri-Bold',):
    """
    Create a title clip
    """
    clip = TextClip(title, fontsize=70, color=color,
                    font=font).set_duration(duration)
    return clip
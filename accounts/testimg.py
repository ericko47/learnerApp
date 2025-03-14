import glob
import os
import subprocess


def conCat():
    filename = '../lectures/final_files/erickVideo.mp4'
    cmd = "ffmpeg -f concat -safe 0 -i videos.txt -c copy " + filename
    subprocess.call(cmd, shell=True)

conCat()

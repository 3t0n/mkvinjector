#!/usr/bin/env python

"""
Script to inject subtitles and audio to mkv files.
Resources should have the same name as target mkv container.

Based on ffmpeg command:
ffmpeg -i input.mkv -i audio.dts -map 0 -map 1 -c copy output.mkv

"""

import sys
import subprocess
from distutils.spawn import find_executable
import os
from os import listdir, walk, makedirs
from os.path import isfile, join, dirname, abspath, basename, splitext, exists


current_path = dirname(abspath(__file__))
output_path = join(current_path, "out")

# Try to search ffmpeg
def find_ffmpeg():
    if os.name == "nt":
        exe = "ffmpeg.exe"
    else:
        exe = "ffmpeg"

    # Current directory
    ffmpeg_path = find_executable(exe, current_path)
    if ffmpeg_path:
        ffmpeg_path = join(current_path, ffmpeg_path)

    # Path variable
    if not ffmpeg_path:
        ffmpeg_path = find_executable(exe)

    # Absolute path to resource for PyInstaller
    if not ffmpeg_path:
        base_path = getattr(sys, '_MEIPASS', current_path)
        ffmpeg_path = join(base_path, exe)

    if not ffmpeg_path:
        ffmpeg_path = exe

    #print(ffmpeg_path)
    return ffmpeg_path

# Get list of current directory files
def get_files():
    mkv_files = []
    res_files = []

    for dirpath, dirnames, filenames in os.walk(current_path):
        for filename in filenames:
            if dirpath == output_path:
                pass
            elif dirpath == current_path and filename.endswith(".mkv"):
                mkv_files.append(join(dirpath, filename))
            else:
                res_files.append(join(dirpath, filename))

    return mkv_files, res_files

# Create output folder
def create_folder(directory):
    if not exists(directory):
        try:
            makedirs(directory)
        except Exception:
            print("Oooops! Cant create output folder")
            sys.exit(1)

mkv_files, res_files  = get_files()
mkv_files.sort()
#print(res_files)
#print(mkv_files)

if len(mkv_files) == 0:
    print('No mkv files found!')
    sys.exit(0)

# Main loop over all root mkv files
for mkv in mkv_files:
    # cmd = ['-i', mkv]
    cmd = ['-loglevel', 'panic', '-i', mkv]

    # Get only mkv name without extension
    mkv_basename = basename(mkv)
    mkv_onlyname = splitext(mkv_basename)[0]
    print('\n--> Processing: \"{}\"'.format(mkv_basename))

    # Get all resources for this mkv, files with similar names but different ext.
    mkv_resources = [f for f in res_files if basename(f).startswith(mkv_onlyname)]
    if len(mkv_resources) > 0:
        # Get -i params
        for res in mkv_resources:
            print("--> Resource found: \"{}\"".format(res))
            cmd.extend(['-i', res])

        # Get -map params
        for i in range(len(mkv_resources) + 1):
            cmd.extend(['-map', str(i)])

        # Get mkv output name & create output folder
        mkv_output = join(output_path, mkv_basename)
        create_folder(output_path)

        # Add last part of command
        cmd.extend(['-c', 'copy', mkv_output])
        cmd.insert(0, find_ffmpeg())
        #print(cmd)

        # Start ffmpeg process
        err = subprocess.call(cmd, shell=False)

        # err 256 == skip rewrite
        if err not in [0, 256]:
            print("Oooops! Something going wrong! Exit code: {0}".format(err))
            sys.exit(err)

    else:
        print('No resources found! Resources should have the same name as target mkv container!')

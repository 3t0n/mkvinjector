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
from os import listdir
from os.path import isfile, join, dirname, abspath, basename, splitext


current_path = dirname(abspath(__file__))

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

all_files = [f for f in listdir(current_path) if isfile(join(current_path, f))]
#print (all_files)

mkv_files = [f for f in all_files if f.endswith(".mkv")]
mkv_files.sort()
#print (mkv_files)

for mkv in mkv_files:
    # cmd = ['-i', mkv]
    cmd = ['-loglevel', 'panic', '-i', mkv]

    print('\n--> Processing \"{}\":'.format(mkv))

    mkv_name = splitext(basename(mkv))[0]
    res_files = [f for f in all_files if f != mkv and f.startswith(mkv_name)]
    #print (res_files)

    if len(res_files) > 0:
        for res in res_files:
            cmd.extend(['-i', res])

        for i in range(len(res_files) + 1):
            cmd.extend(['-map', str(i)])

        cmd.extend(['-c', 'copy', 'new-' + mkv])
        cmd.insert(0, find_ffmpeg())
        print(cmd)

        err = subprocess.call(cmd, shell=False)

        # err 256 == skip rewrite
        if err not in [0, 256]:
            print("Oooops! Something going wrong! Exit code: {0}".format(err))
            sys.exit(err)

    else:
        print('No resources found! Resources should have the same name as target mkv container!')

#!/bin/bash

# Here should be your path to pyinstaller
/Library/Frameworks/Python.framework/Versions/3.6/bin/pyinstaller -F --add-binary="ffmpeg:."  mkvinjector.py
#"C:\Program Files\Python\Scripts\pyinstaller"  -F --add-binary="ffmpeg.exe;."  mkvinjector.py

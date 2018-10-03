---
Introduction
---
MkvInjector is a tool for injecting resources like subtitles and audio to mkv files.
Simple copy script to destination directory with mkv files, their resources and run.
Resources should have the same name as target mkv container.

Based on ffmpeg command:
	ffmpeg -i input.mkv -i audio.dts -map 0 -map 1 -c copy output.mkv

---
Windows
---
Download Python executable installer for windows:
	https://www.python.org/downloads/windows
Python should be associated with '.py' extention.

Download ffmpeg installer for windows with static linking:
	https://www.ffmpeg.org/download.html
Add ffmpeg to windows path:
	https://www.wdiaz.org/how-to-install-ffmpeg-on-windows/

---
macOS
---
Install Python and ffmpeg:
You can use a packager like [Homebrew](https://brew.sh/) to find these packages.

        brew install python ffmpeg

---
Linux
---
Install Python and ffmpeg:
	apt-get install python ffmpeg

---
Run
---
Copy script to destination directory, then run:
        ./mkvinjector.py


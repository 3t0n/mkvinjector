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
TBD

---
macOS
---
To run in macOS install the python and ffmpeg.
You can use a packager like [Homebrew](https://brew.sh/) to find these packages.

        brew install python ffmpeg

---
Linux
---

	apt-get install ffmpeg

---
Run
---
Copy script to destination directory, then run:

        ./mkvinjector.py



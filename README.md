# 🎞️ Video Resolution Converter (Python + FFmpeg)

A simple and efficient command-line tool to convert videos into multiple resolutions (480p, 720p, 1080p) using Python and FFmpeg.

---

## 🚀 Features

- 🔄 Convert video to:
  - 480p
  - 720p
  - 1080p
  - All 3 resolutions at once
- 📦 Outputs file size of each version

---

## 📸 Demo

```bash
$ python main.py
Enter Video address: sample.mp4
Enter video name: output
Enter Number Which Quality To convert:
 0 for Gpu mode
 1 for 480 
 2 for 720 
 3 for 1080 
 if you all quality then Enter 4 
 What you want? : 4

==================================================
✅ Conversion Successful in 3 Qualities!
Generated Files:
output_480.mp4: 12.34 MB
output_720.mp4: 25.67 MB
output_1080.mp4: 48.12 MB
==================================================

Generate movie palettes from this script.

Suggestions for video file:
* Resize to 720p
* Set it to 1 frame per second i.e. choose one frame for each second. While this may lead to some loss in information, I don't believe its signifcant. Plus you can set it to whatever you want and see the output for yourself.

FFMPEG command to implement above suggestions:
```bash
ffmpeg -i input.mp4 -vf "fps=1,scale=iw/4:ih/4" output.mp4
```

I used the scale command to scale down the res to a quarter of the original.
# Jellyfish

### Timeline Video

```bash
manimgl timeline.py Timeline -r 1280x720 -w
```

### Timeline Composition

```bash
ffmpeg -i videos/Timeline.mp4 -i videos/gear.wav -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 videos/tl.mp4
```

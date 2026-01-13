# Jellyfish

### Timeline Video

```bash
manimgl timeline.py Timeline -r 1280x720 -w
```

### Timeline Composition

```bash
ffmpeg -i videos/Timeline.mp4 -i videos/gear.wav -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 videos/tl.mp4
```

## Blender Setup

1. Press `Cmd+Shift+P` → "Python: Select Interpreter"
   - `/Applications/Blender.app/Contents/Resources/3.6/python/bin/python3.10`
2. `/Applications/Blender.app/Contents/Resources/3.6/python/bin/python3.10 -m pip install fake-bpy-module-3.6`
3. Python > Analysis: Extra Paths
   - `/Applications/Blender.app/Contents/Resources/3.6/scripts/modules`
   - `/Applications/Blender.app/Contents/Resources/3.6/python/lib/python3.10/site-packages`

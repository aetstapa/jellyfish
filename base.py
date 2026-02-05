from manimlib import *
import os, re

project_dir = "/Users/jiaju/Documents/视频/001.李白/李白/"


def cook(scene: Scene, basename: str):
    pattern = re.compile(rf"{re.escape(basename)}_v(\d+)\.mp4$")
    version = 1
    for filename in os.listdir(project_dir):
        match = pattern.match(filename)
        if match:
            ver = int(match.group(1))
            if ver >= version:
                version = ver + 1
            os.remove(os.path.join(project_dir, filename))

    scene(
        camera_config={"resolution": (1920, 1080)},
        file_writer_config={
            "write_to_movie": True,
            "output_directory": project_dir,
            "file_name": f"{basename}_v{version}",
        },
    ).run()

import cv2
import os
from urllib.parse import urlparse


class Thumbnailer:
    def __init__(self, rows=3, cols=3):
        self.rows = rows
        self.cols = cols

    def generate(self, video_path, output_path):
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        timestamps = []
        for i in range(self.rows):
            for j in range(self.cols):
                timestamp = i * total_frames // self.rows + j * total_frames // self.cols // self.rows
                timestamps.append(timestamp)

        screenshot_collage = None
        row = None
        for i, timestamp in enumerate(timestamps):
            cap.set(cv2.CAP_PROP_POS_FRAMES, timestamp)
            ret, frame = cap.read()
            if ret:
                # Resize frame to fit in the grid
                frame = cv2.resize(frame, (frame_width // self.cols, frame_height // self.rows))
                # Convert frame to same type as the first frame
                if screenshot_collage is not None:
                    frame = cv2.convertScaleAbs(frame, alpha=(255.0/screenshot_collage.max()))
                # Add frame to row
                if row is None:
                    row = frame
                else:
                    row = cv2.hconcat([row, frame])
                # Add row to screenshot collage
                if i % self.cols == self.cols - 1:
                    if screenshot_collage is None:
                        screenshot_collage = row
                    else:
                        screenshot_collage = cv2.vconcat([screenshot_collage, row])
                    row = None
            else:
                print(f"Failed to read frame at timestamp {timestamp}.")

        cv2.imwrite(output_path, screenshot_collage)


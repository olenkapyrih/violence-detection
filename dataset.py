import os
from enum import Enum
import re
from collections import Counter
import cv2


class DataClasses(Enum):
    NO_VIOLENCE = 'A'
    FIGHTING = 'B1'
    SHOOTING = 'B2'
    RIOT = 'B4'
    ABUSE = 'B5'
    CAR_ACCIDENT = 'B6'
    EXPLOSION = 'G'


def extract_label(filename: str):
    match = re.search(r'label_([A-Z0-9-]+)', filename)
    if match:
        return match.group(1).split('-')
    return []


class Dataset:
    def __init__(self, folder_path: str):
        self.path = folder_path
        self.data = self.get_filenames()

    def get_filenames(self) -> list[str]:
        return os.listdir(self.path)

    def count_entries(self) -> dict[Enum: int]:
        class_counter = Counter()
        for filename in self.data:
            labels = extract_label(filename)
            for label in labels:
                if label != '0':
                    class_counter[label] += 1
        return class_counter

    def count_video_frames(self, video_path: str) -> int:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video {video_path}")
            return 0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get frame count
        cap.release()
        return frame_count

    def find_longest_video(self) -> int:
        frame_count = 0
        # print(self.data)
        for video_path in self.data:
            full_path = self.path + '/' + video_path
            temp = self.count_video_frames(full_path)
            frame_count = temp if temp > frame_count else frame_count
        return frame_count

parser = Dataset("C:/Users/Olenka/Downloads/1-1004 (1)")

print("Class Distribution in Dataset:")
for label, count in sorted(parser.count_entries().items()):
    print(f"{label}: {count}")

print(parser.find_longest_video())
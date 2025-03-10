import os
import random
import re
import shutil
from collections import Counter, defaultdict
from enum import Enum

import cv2

"""
Оскільки я не маю достатньо ресурсів для того, щоб ефективно тренувати моделі на всьому об'ємі датасету, було
вирішено взяти його частину, а саме - відео, довжина яких складає не більше, ніж 2 хвилини. В оригінальному
наборі даних клас В5 є мінорним (зразків цього класу є найменше), то будуть взяті всі його відео, а відео з решти
класів будуть взяті таким чином:
        A: 222
        B1: 74
        B2: 74
        B4: 74
        B5: 37
        B6: 74
        G: 74
Відповідно, маємо набір даних, який складається з 639 відео, при цьому довжина кожного становить не більше 2 хв. 
"""


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
    def __init__(self, folders: list[str], threshold: int = 2340):
        self.folders = folders
        self.threshold = threshold
        self.data_classes = defaultdict(list)
        self.data = self.get_filenames()

    def get_filenames(self) -> list[str]:
        filenames = []
        for folder in self.folders:
            for filename in os.listdir(folder):
                filenames.append(f'{folder}/{filename}')
        return filenames

    def count_entries(self) -> dict[Enum: int]:
        class_counter = Counter()
        for filename in self.data:
            # print(filename)
            labels = extract_label(filename)
            for label in labels:
                if label != '0' and self.count_video_frames(filename) <= self.threshold:
                    class_counter[label] += 1
        return class_counter

    def count_video_frames(self, video_path: str) -> int:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video {video_path}")
            return 0
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        return frame_count

    def organize_videos(self, output_folder: str):
        for label in DataClasses:
            label_folder = os.path.join(output_folder, label.value)
            if not os.path.exists(label_folder):
                os.makedirs(label_folder)

        label_videos = defaultdict(list)
        for filename in self.data:
            labels = extract_label(filename)
            for label in labels:
                label_videos[label].append(filename)

        data_samples = {
            'A': 222,
            'B1': 74,
            'B2': 74,
            'B4': 74,
            'B5': 37,
            'B6': 74,
            'G': 74
        }
        for label, videos in label_videos.items():
            if label in data_samples:
                videos_to_copy = random.sample(videos, min(data_samples[label], len(videos)))
                for video in videos_to_copy:
                    label_folder = os.path.join(output_folder, label)
                    shutil.copy(video, os.path.join(label_folder, os.path.basename(video)))


folders = ["C:/Users/Olenka/Downloads/1-1004",
           "C:/Users/Olenka/Downloads/1005-2004",
           "C:/Users/Olenka/Downloads/2005-2804",
           "C:/Users/Olenka/Downloads/2805-3319",
           "C:/Users/Olenka/Downloads/3320-3954"]

parser = Dataset(folders)
parser.organize_videos("C:/Users/Olenka/PycharmProjects/violence_detection/dataset")

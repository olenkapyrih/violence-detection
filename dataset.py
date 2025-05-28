import os
import shutil
import random
import cv2


folders = [
    r"C:\Users\Olenka\Downloads\1-1004",
    r"C:\Users\Olenka\Downloads\1005-2004",
    r"C:\Users\Olenka\Downloads\2005-2804",
    r"C:\Users\Olenka\Downloads\2805-3319",
    r"C:\Users\Olenka\Downloads\3320-3954",
]
output = "dataset"
classes = ['A', 'B1', 'B2', 'B4', 'B5', 'B6', 'G']

def extract_labels(file):
    parts = file[:-4].split("label_")

    if len(parts) < 2:
        return [0] * len(classes)

    return [1 if cls in parts[1].split('-') else 0 for cls in classes]

def get_video_duration_sec(video_path: str) -> float:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Warning: Cannot open video {video_path}")
        return 0
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.release()
    return frame_count / fps if fps else 0


all_files = [(os.path.join(folder, file), file) for folder in folders for file in os.listdir(folder) if get_video_duration_sec(os.path.join(folder, file)) <= 60]
random.shuffle(all_files)

labels = {path: extract_labels(path) for path, _ in all_files}

curr_classes = [0] * len(classes)
selected_files = set()
i = 0

while any(cnt < 100 for cnt in curr_classes) and i < len(all_files):
    path, name = all_files[i]
    ls = labels[path]

    if sum(ls) == 1:
        for j, label in enumerate(ls):
            if label == 1 and curr_classes[j] < 100:
                selected_files.add((path, name))
                curr_classes[j] += 1

    i += 1
print(curr_classes)

for path, name in selected_files:
    shutil.copy2(path, os.path.join(output, name))

import os
import shutil

directories = ["C:/Users/Olenka/PycharmProjects/violence_detection/train",
               "C:/Users/Olenka/PycharmProjects/violence_detection/validation",
               "C:/Users/Olenka/PycharmProjects/violence_detection/test"]

for folder in directories:
    for filename in os.listdir(folder):
        old_path = os.path.join(folder, filename)
        new_filename = filename.replace("#", "")
        new_path = os.path.join(folder, new_filename)

        if old_path != new_path:
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                print(f"Renamed {old_path} to {new_path}")
            else:
                print(f"Skipped renaming {old_path}: {new_path} already exists")
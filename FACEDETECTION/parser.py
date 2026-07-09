import os
import pandas as pd
from PIL import Image

FILEPATHS = ['Dataset/part1', 'Dataset/part2', 'Dataset/part3']
records = []
skipped_name = 0
skipped_file = 0

for filepath in FILEPATHS:
    for img_name in os.listdir(filepath):
        if not img_name.endswith('.jpg'):
            continue
        parts = img_name.split('_')
        try:
            age = int(parts[0])
            gender = int(parts[1])
            # full_path = os.path.join(filepath, img_name)
            full_path = f"{filepath}/{img_name}"  
            with Image.open(full_path) as im:
                im.verify()
            records.append({'img_path': full_path, 'age': age, 'gender': gender})
        except (ValueError, IndexError):
            skipped_name += 1
            continue
        except (OSError, Image.UnidentifiedImageError):
            skipped_file += 1
            continue

df = pd.DataFrame(records)
print(f"Собрано {len(df)} записей")
print(f"Пропущено по имени: {skipped_name}, по битому файлу: {skipped_file}")
df.to_csv('data.csv', index=False)
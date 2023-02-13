import json
import glob
from datetime import datetime
import csv
import time

import pandas as pd

start = time.time()  # start time
print('Start conversion, json to csv')

# Place your JSON data in a directory named 'data/'
src = "data/"

date = datetime.now()
data = []

# Change the glob if you want to only look through files with specific names
files = glob.glob('data/*', recursive=True)

# Loop through files
cnt = 0
err_cnt = 0
for single_file in files:
    cnt += 1
    with open(single_file, 'r') as f:

        # Use 'try-except' to skip files that may be missing data
        try:
            json_file = json.load(f)
            temp = []
            temp.extend([
                json_file['audio']['fileSize'],
                json_file['audio']['duration'],
                json_file['annotations'][0]['audio_id'],
                json_file['annotations'][0]['area']['start'],
                json_file['annotations'][0]['area']['end'],
                json_file['annotations'][0]['categories']['category_01'],
                json_file['annotations'][0]['categories']['category_02'],
                json_file['annotations'][0]['categories']['category_03'],
                json_file['annotations'][0]['note'],
                json_file['annotations'][0]['audioType']
            ])
            # Not in '실내' category, occurs key error
            try:
                temp.extend([
                    json_file['annotations'][0]['gender'],
                    json_file['annotations'][0]['generation'],
                    json_file['annotations'][0]['dialect']
                ])
            # fill with None for exception
            except KeyError:
                temp.extend([None, None, None])

            data.append(temp)

        except KeyError as e:
            print(e)
            err_cnt += 1
            print(f'Skipping {single_file}')

# Sort the data
data.sort()

# Add headers
data.insert(0, ['fileSize', 'duration', 'audio_id', 'area_start', 'area_end',
                'category_01', 'category_02', 'category_03', 'note', 'audioType', 'gender', 'generation', 'dialect'])

# Export to CSV.
# Add the date to the file name to avoid overwriting it each time.
today = datetime.today().strftime("%Y-%m-%d")
csv_filename = f'{today}_6axis_data.csv'
with open(csv_filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

print(f"Updated CSV, {cnt} json files converted, {err_cnt} files skipped")
print("total time :", round(float(time.time() - start), 2))

# read CSV by pandas
df = pd.read_csv(csv_filename, encoding='utf8', low_memory=False)
pd.set_option('display.max_columns', None)
print(df)
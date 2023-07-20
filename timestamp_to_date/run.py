import datetime
import os

for root, dirs, files in os.walk("/Users/chenhaiou/Documents/mv"):
    for file in files:
        file_path = os.path.join(root, file)
        if 'DS_Store' in file_path:
            continue
        else:
            timestamp = file_path.split('mmexport')[-1].split('.')[0]
            timestamp = timestamp.split('/')[-1]
            timestamp = int(timestamp[:-3])
            date = str(datetime.datetime.fromtimestamp(timestamp))[:10]

        file_path_split = file_path.split('/')
        file_path_split[-1] = f"{date} {file_path_split[-1]}"
        to_file_path = '/'.join(file_path_split)

        print(f'{file_path=}; {timestamp=}; {to_file_path}')
        os.rename(file_path, to_file_path)
        input()

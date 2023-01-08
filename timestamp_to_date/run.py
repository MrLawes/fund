import datetime
import os

for root, dirs, files in os.walk("/Users/chenhaiou/Documents/陈海鸥手机"):
    for file in files:
        file_path = os.path.join(root, file)
        if '_2022' in file_path:
            continue
        if 'DS_Store' in file_path:
            continue
        timestamp = file_path.split('mmexport')[-1].split('.')[0]
        timestamp = timestamp.split('/')[-1]
        timestamp = int(timestamp[:-3])
        date = str(datetime.datetime.fromtimestamp(timestamp).date())
        to_file_path = file_path.replace('月/', f'月/{date} ')
        # print(f'{file_path=}; {timestamp=}; {to_file_path}')
        os.rename(file_path, to_file_path)
        # input()

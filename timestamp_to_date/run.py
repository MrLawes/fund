import datetime
import os

for root, dirs, files in os.walk("/Users/chenhaiou/Documents/陈海鸥手机"):
    for file in files:
        file_path = os.path.join(root, file)
        if 'DS_Store' in file_path:
            continue
        if '_2022' in file_path:
            timestamp = file_path.split('_')[1]
            timestamp = f'{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]}'
            to_file_path = file_path.replace('月/', f'月/{timestamp} ')
        else:
            timestamp = file_path.split('mmexport')[-1].split('.')[0]
            timestamp = timestamp.split('/')[-1]
            timestamp = int(timestamp[:-3])
            date = str(datetime.datetime.fromtimestamp(timestamp).date())
            to_file_path = file_path.replace('月/', f'月/{date} ')

        print(f'{file_path=}; {timestamp=}; {to_file_path}')
        # os.rename(file_path, to_file_path)
        # input()

import datetime
import os

for root, dirs, files in os.walk("/Users/chenhaiou/Documents/mv/pic"):
    for file in files:
        file_path = os.path.join(root, file)
        if 'DS_Store' in file_path:
            continue
        if '_2023' in file_path:
            timestamp = file_path.split('_')[1]
            date = f'{timestamp[:4]}-{timestamp[4:6]}-{timestamp[6:8]}'
            # to_file_path = file_path.replace('月/', f'月/{timestamp} ')
        else:
            timestamp = file_path.split('mmexport')[-1].split('.')[0]
            timestamp = timestamp.split('/')[-1]
            if timestamp[:-3] in ('2019-05-29 陈海鸥结业', '2019-05-29 陈海鸥结业', '2023-01-01 馨菲第一次吃'):
                continue
            timestamp = int(timestamp[:-3])
            date = str(datetime.datetime.fromtimestamp(timestamp))[:10]

        file_path_split = file_path.split('/')
        file_path_split[-1] = f"{date} {file_path_split[-1]}"
        to_file_path = '/'.join(file_path_split)

        print(f'{file_path=}; {timestamp=}; {to_file_path}')
        # os.rename(file_path, to_file_path)
        # input()

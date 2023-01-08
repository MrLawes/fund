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
        print(f'{file_path=}; {timestamp=}')

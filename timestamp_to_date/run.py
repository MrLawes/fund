import datetime
import os

for root, dirs, files in os.walk("/Users/chenhaiou/Documents/视频/2025-03/"):
    for file in files:
        file_path = os.path.join(root, file)
        # print(f"{file_path=}")
        if 'DS_Store' in file_path:
            continue
        elif "IMG_" in file_path or "VID_" in file_path or "Screenshot_" in file_path:
            date = file_path.split('_')[1]
            date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        elif file_path.split('/')[-1].startswith("202"):
            continue
        else:
            if "wx_camera_" in file_path:
                timestamp = file_path.split('wx_camera_')[-1].split('.')[0]
            elif "Image_" in file_path:
                timestamp = file_path.split('Image_')[-1].split('.')[0]
            else:
                timestamp = file_path.split('mmexport')[-1].split('.')[0]
                if '_' in timestamp:
                    timestamp = timestamp.split('_')[-1]
            timestamp = timestamp.split('/')[-1]
            timestamp = int(timestamp[:10])
            date = str(datetime.datetime.fromtimestamp(timestamp))[:10]

        file_path_split = file_path.split('/')
        file_path_split[-1] = f"{date} {file_path_split[-1]}"
        file_path_split[-1] = f"{date} {file_path_split[-1].split(' ')[-1]}"
        to_file_path = '/'.join(file_path_split)
        print(f'{file_path=}; {to_file_path}')
        # os.rename(file_path, to_file_path)

print("完成")

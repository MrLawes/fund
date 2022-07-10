# Create your tests here.

# 图片处理

import os


def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f == '.DS_Store':
                continue
            full_file_name = f'{root}/{f}'
            yield full_file_name


base = '/Users/chenhaiou/Downloads/D盘/照片/2022'
for f_name in findAllFile(base):
    print(f'{f_name=}')

    # if not 'mmexport' in f_name:
    #     continue
    # new_f_name = f_name.replace('mmexport', ' ')
    # t = int(new_f_name.split('.')[0]) / 1000
    # time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    # print(f_name, t, time_str)
    # input()
    # os.rename(
    #     f"/Users/chenhaiou/Downloads/D盘/照片/2022/2022年06月/{f_name}",
    #     f"/Users/chenhaiou/Downloads/D盘/照片/2022/2022年06月/{time_str} {f_name}"
    # )

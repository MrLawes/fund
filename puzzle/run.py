import copy
import datetime
import itertools


class ChessBoard:

    def __init__(self):

        # 棋盘布局，1：代表不能放入；0：代表空着，允许放入
        self.data = [
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0],
        ]
        now = datetime.datetime.now()

        # 将棋盘对应的月份填上
        month = now.month
        if month <= 6:
            self.data[0][month - 1] = 1
        else:
            self.data[1][month - 7] = 1

        # 将棋盘对应的几号填上
        day = now.day
        if day <= 7:
            self.data[2][day - 1] = 1
        elif day <= 14:
            self.data[3][day - 8] = 1
        elif day <= 21:
            self.data[4][day - 15] = 1
        elif day <= 28:
            self.data[5][day - 22] = 1
        elif day <= 31:
            self.data[6][day - 29] = 1

        # 将棋盘对应的星期填上
        weekday = now.weekday() + 1
        if weekday == 7:
            weekday = 0
        if weekday <= 3:
            self.data[6][weekday + 3] = 1
        else:
            self.data[7][weekday] = 1

        self.print_data()

    def print_data(self):
        print('当前棋盘:')
        for i in self.data:
            print(i)

    @property
    def blank_index(self):
        """ 第一个空白位
        """
        for row, data in enumerate(self.data):
            if 0 in data:
                return row, data.index(0)
        else:
            return -1, -1

    def put_chess(self, items):

        blank_index = self.blank_index

        for item_row, item in enumerate(items):
            for item_cow, value in enumerate(item):
                if value == 0:
                    continue

                row = blank_index[0] + item_row
                col = blank_index[1] + item_cow
                if self.data[row][col]:
                    print('已存在棋子')
                    return False
                self.data[row][col] = value

        print('放入棋子:')
        for i in items:
            print(i)

        self.print_data()

        if blank_index == (-1, -1):
            with open('resutl.log', 'a+') as f:
                f.write('完成棋子')
                for i in items:
                    f.write(i)
        return True


class Chess:

    def __init__(self, data):

        self.data = []
        self.data.append(data)
        # 逆时针旋转 90 度
        for i in range(1, 4):
            data = list(map(list, zip(*data)))[::-1]
            self.data.append(data)

        # 水平翻转
        copy_data = copy.deepcopy(data)
        for index, d in enumerate(copy_data):
            d.reverse()
        self.data.append(copy_data)

        # 逆时针旋转 90 度
        for i in range(1, 4):
            copy_data = list(map(list, zip(*copy_data)))[::-1]
            self.data.append(copy_data)

        unique_data = []

        for data in self.data:
            if not data in unique_data:
                unique_data.append(data)

        self.data = unique_data


chess_data = []
chess_data.append([
    [1, 1, 1],
    [0, 0, 1],
    [0, 0, 1],
])
chess_data.append([
    [2, 0, 2],
    [2, 2, 2],
])
chess_data.append([
    [3, 3, 3],
    [0, 0, 3],
])
chess_data.append([
    [4, 4, 4],
    [0, 0, 4],
])
chess_data.append([
    [0, 0, 0, 5],
    [5, 5, 5, 5],
])
chess_data.append([
    [0, 6, 6],
    [0, 6, 0],
    [6, 6, 0],
])
chess_data.append([
    [7, 7, 7, 7],
])
chess_data.append([
    [8, 8, 0],
    [0, 8, 8],
])
chess_data.append([
    [0, 9, 9],
    [9, 9, 9],
])
chess_data.append([
    [0, 10, 10, 10],
    [10, 10, 0, 0],
])
chess_data.append([
    [0, 11, 0],
    [0, 11, 0],
    [11, 11, 11],
])
chess_list = []
for data in chess_data:
    chess_list.append(Chess(data=data))

# 遍历出所有的组合
for chesses in itertools.permutations(chess_list, len(chess_list)):
    data = []
    for chess in chesses:
        data.append(chess.data)

    error_chess = None, None
    for items in itertools.product(*data):
        if error_chess[0]:
            if items[error_chess[0]] == error_chess[1]:
                continue
        chess_board = ChessBoard()
        for index, item in enumerate(items):
            result = chess_board.put_chess(item)
            if not result:
                break

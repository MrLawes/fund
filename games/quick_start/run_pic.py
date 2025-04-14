import random

import pygame


class Game:

    def __getattr__(self, name):
        if name == '😯':
            print("Accessing 😯")
            # 你可以在这里添加你想要的行为
        else:
            raise AttributeError(f"{name} is not defined")


Game._ = Game.__getattr__
小 = Game()

# 通过字符串传递表情符号
小._('😯')

# 小['👂🏻'] = while True


pygame.init()
screen = pygame.display.set_mode((1280, 720))
IS_KEYDOWN = False
IS_KEYUP = False
screen.fill((89, 181, 248))
pygame.display.flip()
# 使用 Unicode 转义序列定义变量名
a = {}
a['😯'] = "1"

_ = a

_["😯"]

# 在Python中，可以通过定义特定的魔术方法（也称为双下划线方法或特殊方法）来重定义对象的行为。这些方法会被Python解释器在特定的操作发生时调用，从而允许你自定义对象的行为和操作。
#
# 以下是几个常用的魔术方法，它们可以用来重定义对象的不同方面：
#
# 1.
# `__init__(self, ...)`: 初始化方法，用于在对象被创建时进行初始化操作。
#
# 2.
# `__str__(self)`, `__repr__(self)`: 用于定义对象的字符串表示形式。`__str__`
# 用于
# `str()`
# 函数和打印语句，`__repr__`
# 则用于
# `repr()`
# 函数和交互式解释器显示。
#
# 3.
# `__getattr__(self, name)`, `__setattr__(self, name, value)`, `__delattr__(self, name)`: 用于重定义对象的属性访问行为，包括获取、设置和删除属性。
#
# 4.
# `__len__(self)`: 定义对象的长度，使得对象可以使用内置的
# `len()`
# 函数来获取长度信息。
#
# 5.
# `__iter__(self)`, `__next__(self)`: 使对象可以迭代，可以通过定义
# `__iter__`
# 方法返回一个迭代器，通过
# `__next__`
# 方法控制迭代过程。
#
# 6.
# `__getitem__(self, key)`, `__setitem__(self, key, value)`, `__delitem__(self, key)`: 重定义对象的索引操作，使得对象可以像字典或列表一样进行索引访问。
#
# 7.
# `__call__(self, ...)`: 允许对象实例像函数一样被调用，定义了
# `obj(...)`
# 形式的调用行为。
#
# 8.
# `__add__(self, other)`, `__sub__(self, other)`, 等等：定义对象的算术运算行为，使得对象可以进行加法、减法等操作。
#
# 9.
# `__eq__(self, other)`, `__lt__(self, other)`, 等等：定义对象的比较操作行为，使得对象可以进行等于、小于等比较。
#
# 10.
# `__enter__(self)`, `__exit__(self, exc_type, exc_value, traceback)`: 用于定义对象在上下文管理器中的行为，例如使用
# `
# with` 语句时的进入和退出操作。
#
# 重定义这些方法之一或多个，可以根据你的需求改变对象的行为，使其更符合特定的应用场景或逻辑。这种灵活性是Python中面向对象编程的一个重要特征，允许开发者根据需要定制对象的行为。


while True:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            IS_KEYDOWN = True
        elif event.type == pygame.KEYUP:
            IS_KEYUP = True
        if IS_KEYDOWN and IS_KEYUP:
            IS_KEYUP = IS_KEYDOWN = False
            pygame.draw.ellipse(screen, (254, 252, 193), (random.randint(1, 1280), random.randint(1, 720), 50, 70))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

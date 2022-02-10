import datetime

from rich.console import Console
from rich.table import Table

年利息 = 0.04
月利息 = (1 + 年利息) ** (1.0 / 12.0) - 1
会员人数 = 12
利息 = 1500
每次付会金额 = 10000

for person_index in range(1, 会员人数 + 1):

    开始时间 = datetime.datetime(2019, 9, 15)

    table = Table(title="")
    table.add_column("姓名", justify="left", no_wrap=True, )
    table.add_column("时间", justify="right", style="red", no_wrap=True)
    table.add_column("得会金额", justify="right", style="cyan", no_wrap=True)
    table.add_column("付会金额+利息", justify="right", style="cyan", no_wrap=True)
    table.add_column(f"存入银行利息(月利息={月利息:0.04f})", justify="right", style="cyan", no_wrap=True)
    table.add_column("最终金额（初始金额12万）", justify="right", style="red", no_wrap=True)

    for month in range(1, 会员人数 * 4 + 1):

        if (person_index - 1) * 4 == month - 1:
            是否得会 = True
            if person_index == 1:
                得会金额 = (person_index - 1) * 利息 + 每次付会金额 * (会员人数 - 1)
            else:
                得会金额 = (person_index - 2) * 利息 + 每次付会金额 * (会员人数 - 1)
        else:
            是否得会 = False
            得会金额 = 0

        if (person_index - 1) * 4 == month - 1:
            table.add_row(f'会员[{person_index}] ', f'{开始时间.date()}', f'{得会金额}', 'xx', 'ss', 'dd')

        开始时间 = 开始时间 + datetime.timedelta(days=30)
        开始时间 = 开始时间.replace(day=15)

    console = Console()
    console.print(table)

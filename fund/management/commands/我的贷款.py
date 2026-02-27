import datetime

from dateutil.relativedelta import relativedelta

start_at = datetime.datetime(2026, 1, 1)
end_at = datetime.datetime(2048, 2, 26)

# 使用 relativedelta 计算差异
diff = relativedelta(end_at, start_at)
months = diff.years * 12 + diff.months

# 相差多少天
days = (end_at - start_at).days

# 年利率
annual_rate = 0.032
# 月利率
monthly_rate = annual_rate / 12
# 剩余金额
remaining_amount = 1653493.47
# 应还合计
monthly_repayment = 8709.76

for day in range(1, days + 1):

    current_date = start_at + datetime.timedelta(days=day)

    # 每到月初的时候，计算利息
    if current_date.day == 1:
        # 利息
        interest = round(remaining_amount * monthly_rate, 2)
        # 应还本金
        principal = round(monthly_repayment - interest, 2)
        print("#############################")
        print(f"{current_date.strftime('%Y-%m-%d')} 应还合计(元): {monthly_repayment:,.2f}")
        print(f"应还本金(元): {principal:,.2f}")
        print(f"应还利息(元): {interest:,.2f}")
        print(f"本金余额(元): {remaining_amount:,.2f}")
        # 剩余金额
        remaining_amount -= principal

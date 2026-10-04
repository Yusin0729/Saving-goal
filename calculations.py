"""
程式主要目的與功能：
計算各項儲蓄統計數值，包含累計總存款、剩餘目標金額、平均每次存款金額、目標達成百分比，以及整理出各日累計與每日存款列表。

使用之外部套件：
無使用第三方外部套件，主要引入專案模組 load_target_amount。
"""

from load_target_amount import load_target_amount

def calculate_summary(deposits):
    # 初始化變數
    total_deposits = 0  # 總存款金額
    deposit_data = {}  # 存款數據，以日期為鍵，存款金額為值
    average_deposit = 0  # 平均存款金額
    deposit_amounts = []  # 存款金額列表
    daily_amounts = []  # 每日存款金額列表

    # 遍歷存款列表
    for deposit in deposits:
        total_deposits += float(deposit['deposit_money'])  # 累計總存款金額
        date_key = deposit['date']  # 存款日期作為鍵
        if date_key not in deposit_data:
            deposit_data[date_key] = total_deposits  # 如果日期不在存款數據中，則新增
        else:
            deposit_data[date_key] += float(deposit['deposit_money'])  # 如果日期已存在，則更新金額

        # 添加當天的存款金額到 daily_amounts
        daily_amounts.append(float(deposit['deposit_money']))

    # 提取唯一的存款日期，按升序排序
    unique_dates = sorted(deposit_data.keys())

    # 提取存款金額列表（累加前面日期的金額）
    for date in unique_dates:
        deposit_amounts.append(deposit_data[date])

    remain_target_deposits = load_target_amount() - total_deposits  # 剩餘目標存款金額
    if len(deposits) > 0:
        average_deposits = round(total_deposits / len(deposits), 2)
    else:
        average_deposits = 0

    # 計算完成度百分比
    if load_target_amount() != 0:
        completeness = min(100, round(total_deposits / load_target_amount() * 100, 2))
    else:
        completeness = 0

    # 返回包含結果的列表
    return [total_deposits, remain_target_deposits, average_deposits, completeness, unique_dates, deposit_amounts, daily_amounts]

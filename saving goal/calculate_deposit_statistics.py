"""
程式主要目的與功能：
輔助統計存款數據、計算目標差額、計算完成度以及平均存款金額的函式庫。

使用之外部套件：
無使用外部第三方套件。
"""

def calculate_deposit_statistics(deposits):
    total_deposits = 0
    deposit_data = {}
    average_deposit = 0

    for deposit in deposits:
        average_deposit += 1
        total_deposits += float(deposit['deposit_money'])
        date_key = deposit['date']
        if date_key not in deposit_data:
            deposit_data[date_key] = total_deposits
        else:
            deposit_data[date_key] += float(deposit['deposit_money'])

    unique_dates = list(deposit_data.keys())
    unique_dates.sort()
    deposit_amounts = [deposit_data[date] for date in unique_dates]

    return total_deposits, deposit_amounts, unique_dates

def calculate_target_and_completeness(total_deposits, target_amount):
    remain_target_deposits = target_amount - total_deposits

    if total_deposits / target_amount < 1:
        completeness = round(total_deposits / target_amount * 100, 2)
    else:
        completeness = 100

    return remain_target_deposits, completeness

def calculate_average(total_deposits, average_deposit):
    average_deposits = round(total_deposits / average_deposit, 2)
    return average_deposits

def extract_daily_chart_data(deposits):
    daily_chart_data = [float(deposit['deposit_money']) for deposit in deposits]
    return daily_chart_data

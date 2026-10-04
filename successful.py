"""
程式主要目的與功能：
檢查使用者儲蓄進度是否達到 100%，若達成則將結果標記儲存至 result.csv，並將頁面重定向至祝賀頁面 (/successful)。

使用之外部套件：
1. flask (redirect, url_for): 用於滿足成功條件時重定向使用者瀏覽器至祝賀頁面。
2. csv: 用於讀取與寫入 result.csv，記錄達標狀態。
"""

from flask import redirect, url_for
from calculations import calculate_summary  # 導入必要的模組和函式
from deposits import load_deposits  # 注意: 正確拼寫 deposits
import csv

def successful():
    # 載入存款數據
    deposits = load_deposits()  # 使用你的方式載入 deposits

    # 使用計算摘要的函式
    summary = calculate_summary(deposits)  # 使用你的方式計算 summary

    try:
        # 嘗試讀取 result.csv 中的數據
        with open("result.csv", "r") as result_file:
            result_reader = csv.reader(result_file)
            # 假設 CSV 文件的格式為一行一列的數值
            result = float(next(result_reader)[0])
    except (FileNotFoundError, StopIteration):
        # 如果文件不存在或者沒有內容，將 result 設定為 0
        result = 0

    # 檢查是否滿足成功條件
    if summary[3] == 100 and result == 0:
        with open("result.csv", "w") as result_file:
            writer = csv.writer(result_file)
            writer.writerow([1])  # 將 1 寫入 CSV 文件，表示檢查完成度為 100
        return redirect(url_for('successful_page'))  # 重定向到 successful_page
    return None  # 返回 None，表示未達到成功條件

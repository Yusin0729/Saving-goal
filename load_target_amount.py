"""
程式主要目的與功能：
讀取使用者設定的目標儲蓄金額 (load_target_amount.csv)。

使用之外部套件：
1. csv: 用於讀取 CSV 檔案內容以取得目標金額數值。
"""

import csv

def load_target_amount():
    try:
        with open('load_target_amount.csv', 'r') as file:
            reader = csv.reader(file)
            target_amount = next(reader)[0]  # 假設文件中只有一個值
        return int(target_amount)  # 將目標金額轉換為整數並返回
    except FileNotFoundError:
        return 0  # 如果文件不存在，則返回預設值 0

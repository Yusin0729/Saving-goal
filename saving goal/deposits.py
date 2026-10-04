"""
程式主要目的與功能：
管理存款資料的載入與儲存，支援以日期排序讀取 CSV 存款資料，並儲存更新後的存款記錄。

使用之外部套件：
1. datetime (datetime): 用於解析日期字串以進行存款紀錄的日期排序。
2. csv: 用於讀取 (csv.DictReader) 與寫入 (csv.DictWriter) deposits.csv 檔案。
"""

# 載入存款資料的函數
from datetime import datetime
import csv

def load_deposits():
    try:
        # 嘗試打開 'deposits.csv' 檔案
        with open('deposits.csv', 'r', newline='') as file:
            # 使用 csv.DictReader 將 CSV 檔案轉換為字典列表
            reader = csv.DictReader(file)
            deposits = list(reader)
            # 將存款按日期升序排序
            deposits.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        return deposits
    except FileNotFoundError:
        # 如果檔案不存在，返回空列表
        return []

# 儲存存款資料到 CSV 檔案的函數
def save_deposits(deposits):
    with open('deposits.csv', 'w', newline='') as file:
        # 定義 CSV 檔案的欄位名稱
        fieldnames = ['date', 'deposit_money', 'description']
        # 使用 csv.DictWriter 寫入 CSV 檔案，指定欄位名稱和存款資料
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # 寫入 CSV 檔案的標題行
        writer.writeheader()
        # 寫入存款資料
        writer.writerows(deposits)

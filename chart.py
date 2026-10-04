"""
程式主要目的與功能：
使用 Matplotlib 繪製統計圖表，包括每日存款金額長條圖與累積存款金額折線圖（含目標金額基準線），並轉為 Base64 PNG 格式供前端 HTML 渲染。

使用之外部套件：
1. matplotlib.pyplot: 用於繪製統計圖表 (bar chart, line plot)。
2. io (BytesIO): 用於在記憶體中建立二進位資料流以儲存圖片，免寫入磁碟。
3. base64: 用於將圖表二進位資料編碼為 Base64 字串，嵌入 HTML 網頁中。
"""

import matplotlib.pyplot as plt
from io import BytesIO
import base64

def draw_bar_chart(dates, daily_amounts):
    # 使用 Matplotlib 繪製柱狀圖，X 軸是 dates，Y 軸是每日存款金額，柱的顏色為綠色。
    plt.bar(dates, daily_amounts, color='g')
    
    # 設定圖表標題和軸標籤
    plt.title('Daily Deposit Chart')
    plt.xlabel('Date')
    plt.ylabel('Daily Deposit Amount')
    
    # 設定 X 軸標籤的旋轉、對齊和字體大小
    plt.xticks(rotation='horizontal', ha='right', fontsize=8)
    
    # 使圖表更緊湊
    plt.tight_layout()

    # 在每個柱上方顯示當前存款金額（調整字體大小）
    for date, amount in zip(dates, daily_amounts):
        plt.text(date, amount + 0.1, f"${amount:.2f}", ha='center', va='bottom', rotation='horizontal',
                 fontsize=10)

    # 將圖表保存到 BytesIO 對象中，轉換成 base64 編碼的 PNG 圖片格式。
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_data = base64.b64encode(img_stream.read()).decode('utf-8')
    plt.close()

    return img_data

def draw_line_chart(dates, amounts, target_amount):
    # 使用 Matplotlib 繪製折線圖，X 軸是 dates，Y 軸是 amounts，折線的標記點為圓形，顏色為藍色。
    plt.plot(dates, amounts, marker='o', linestyle='-', color='b')
    
    # 繪製目標存款金額的橫線，顏色為紅色。
    plt.axhline(y=target_amount, color='r', linestyle='-', label='Target Amount')
    
    # 設定圖表標題和軸標籤
    plt.title('Deposit Accumulation Chart')
    plt.xlabel('Date')
    plt.ylabel('Deposit Amount')
    
    # 設定 X 軸標籤的旋轉、對齊和字體F大小
    plt.xticks(rotation='horizontal', ha='right', fontsize=8)
    
    # 使圖表更緊湊
    plt.tight_layout()

    # 在每個數據點上方顯示當前存款金額（調整字體大小）
    for i, txt in enumerate(amounts):
        plt.annotate(f"${txt:.2f}", (dates[i], amounts[i]), textcoords="offset points", xytext=(0, 10), ha='center',
                     fontsize=10)  # 調整字體大小

    # 將圖表保存到 BytesIO 對象中，轉換成 base64 編碼的 PNG 圖片格式。
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_data = base64.b64encode(img_stream.read()).decode('utf-8')
    plt.close()

    return img_data

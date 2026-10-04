"""
程式主要目的與功能：
本程式為 Deposit Tracker (存款追蹤系統) 的主程式與 Flask 路由中樞，負責處理首頁、新增存款、刪除存款、存款分析與目標達成祝賀頁面。

使用之外部套件：
1. flask: 提供 Web 框架功能，包括路由管理、請求處理 (request)、模板渲染 (render_template) 與頁面重定向 (redirect, url_for)。
2. csv: 用於讀取與寫入 CSV 檔案，進行資料持久化儲存。
"""

# 引入 Flask 和其他需要的模組
from flask import Flask, render_template, request, redirect, url_for
import csv
from deposits import load_deposits, save_deposits  
from load_target_amount import load_target_amount
from successful import successful
from chart import draw_bar_chart, draw_line_chart
from calculations import calculate_summary

# 路由設定 - 存款初始化
def clear_all_deposits():  
    # 清空存款數據
    with open("deposits.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'deposit_money', 'description'])
    with open("result.csv", "w") as result_file:
        writer = csv.writer(result_file)
        writer.writerow([0])
    with open("load_target_amount.csv", "w") as target_amount_file:
        # 將 load_target_amount.csv 中的值設定為 0
        writer = csv.writer(target_amount_file)
        writer.writerow([0])

# 建立 Flask 應用程式實例
app = Flask(__name__)

@app.route('/successful')
def successful_page():
    return render_template('successful.html')

# 路由設定 - 首頁
@app.route('/', methods=['GET', 'POST'])
def home():
    clear_deposits = request.args.get('clear_deposits', False)  # 修改這行
    if clear_deposits: 
        clear_all_deposits()

    # 載入存款、目標金額、計算結果
    deposits = load_deposits()  # 修改這行
    user_targetamount = load_target_amount()
    calculations = calculate_summary(deposits)  # 修改這行

    success_result = successful()
    if success_result:
        return success_result
    
    # 如果是 POST 請求，處理更改目標金額
    if request.method == 'POST':
        if 'Change_targetamount' in request.form:
            user_targetamount = int(request.form['user_targetAmount'])
            with open("load_target_amount.csv", "w") as file:
                writer = csv.writer(file)
                writer.writerow([user_targetamount])
    # 傳遞數據到模板
    return render_template('home.html', deposits=deposits, user_targetAmount=user_targetamount, calculations=calculations)  # 修改這行

# 路由設定 - 新增存款
@app.route('/add', methods=['GET', 'POST'])
def add_deposit():  # 修改這行
    if request.method == 'POST':
        # 從表單獲取新增存款的資訊
        date = request.form['date']
        deposit_money = int(request.form['deposit_money'])  # 修改這行
        description = request.form['description']
        deposit = {
            'date': date,
            'deposit_money': deposit_money,  # 修改這行
            'description': description,
        }
        deposits = load_deposits()  # 載入之前的存款數據
        deposits.append(deposit)  # 添加新存款
        save_deposits(deposits)  # 儲存更新後的存款數據

        return redirect(url_for('home'))  # 重定向到首頁

    return render_template('add_deposit.html')  # 修改這行

# 路由設定 - 刪除存款
@app.route('/delete_deposit/<date>', methods=['POST', 'DELETE'])  # 修改這行
def delete_deposit(date):  # 修改這行
    deposits = load_deposits()  # 修改這行
    # 遍歷存款，找到匹配的日期並刪除
    for deposit in deposits:  # 修改這行
        if deposit['date'] == date:  # 修改這行
            deposits.remove(deposit)  # 修改這行
            save_deposits(deposits)  # 修改這行
            break

    return redirect(url_for('home'))  # 重定向到首頁

# 路由設定 - 分析頁面
@app.route('/analysis')
def analysis():
    deposits = load_deposits()  
    calculations = calculate_summary(deposits)  
    user_targetamount = load_target_amount()
    # 繪製柱狀圖
    daily_img_data = draw_bar_chart(calculations[4], calculations[6])

    # 繪製折線圖
    img_data = draw_line_chart(calculations[4], calculations[5], load_target_amount())

    # 傳遞圖片數據和計算結果到模板
    return render_template('analysis.html', user_targetamount=user_targetamount, chart_img_data=img_data,
                           daily_chart_img_data=daily_img_data, calculations=calculations)

# 主程式進入點
if __name__ == '__main__':
    # 啟動 Flask 應用程式
    app.run(debug=True, threaded=False)

import yfinance as yf
import pandas as pd
import time

# 改成相對路徑（同資料夾內）
file_path = "nasdaq_screener.csv"
stock_df = pd.read_csv(file_path)
tickers = stock_df['Symbol'].tolist()

def check_growth(ticker):
    stock = yf.Ticker(ticker)
    try:
        income_stmt = stock.income_stmt
        income_stmt.columns = income_stmt.columns.astype(str)

        if 'Total Revenue' not in income_stmt.index or 'Net Income' not in income_stmt.index:
            print(f"{ticker}: 缺少必要財報資訊")
            return False

        revenue = income_stmt.loc["Total Revenue"].iloc[:3].values[::-1]
        net_income = income_stmt.loc["Net Income"].iloc[:3].values[::-1]

        if len(revenue) < 3 or len(net_income) < 3:
            print(f"{ticker}: 財報資料不足")
            return False

        rev_growth = [(revenue[i+1]-revenue[i])/revenue[i] for i in range(2)]
        income_growth = [(net_income[i+1]-net_income[i])/abs(net_income[i]) for i in range(2)]

        if all(g >= 0.1 for g in rev_growth) and all(g >= 0.1 for g in income_growth):
            print(f"{ticker}: ✅ 通過標準")
            return True
        else:
            print(f"{ticker}: ❌ 未通過標準")
            return False

    except Exception as e:
        print(f"{ticker}: 抓取失敗，原因: {e}")
        return False

qualified_stocks = []

for idx, ticker in enumerate(tickers, start=1):
    print(f"處理第 {idx}/{len(tickers

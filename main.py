import yfinance as yf
import tkinter as tk
from tkinter import Canvas
from threading import Timer
import numpy as np


portfolio = {
    'BHAGYANGR.NS': {'qty': 250, 'avg_price': 109.79},
    'DWARKESH.NS': {'qty': 300, 'avg_price': 74.04},
    'ABBV': {'qty': 1000, 'avg_price': 180}
}


def fetch_stock_data(symbols):
    data = yf.download(symbols, period='1d', interval='1m')
    return data['Adj Close']


def calculate_portfolio_profit_loss(stock_data, portfolio):
    total_value = 0
    total_cost = 0
    
    for symbol, details in portfolio.items():
        if symbol in stock_data and not stock_data[symbol].isnull().all():
            latest_price = stock_data[symbol].dropna().iloc[-1]
            quantity = details['qty']
            avg_price = details['avg_price']
            
            value = latest_price * quantity
            cost = avg_price * quantity
            
            total_value += value
            total_cost += cost
    
    profit_loss_amount = total_value - total_cost
    percentage_return = (profit_loss_amount / total_cost * 100) if total_cost != 0 else 0
    return profit_loss_amount, percentage_return


def update_widget():
    stock_data = fetch_stock_data(symbols)
    profit_loss_amount, percentage_return = calculate_portfolio_profit_loss(stock_data, portfolio)
    
    
    canvas.itemconfig(profit_loss_label, text=f"₹{profit_loss_amount:.2f}")
    canvas.itemconfig(return_label, text=f"{percentage_return:.2f}%")
    
    
    Timer(5, update_widget).start()  


def create_widget():
    global canvas, profit_loss_label, return_label
    
    root = tk.Tk()
    root.title("Portfolio Tracker")
    root.geometry("300x300")
    root.configure(bg='#2E3B55')
    root.attributes('-topmost', True)

    canvas = Canvas(root, width=300, height=300, bg='#2E3B55', highlightthickness=0)
    canvas.pack()

    
    canvas.create_oval(50, 50, 250, 250, outline='white', fill='#2E3B55', width=2)
    
   
    profit_loss_label = canvas.create_text(150, 120, text="", font=("Arial", 20, "bold"), fill="white")
    return_label = canvas.create_text(150, 180, text="", font=("Arial", 16, "bold"), fill="white")

    
    update_widget()
    
    root.mainloop()

symbols = list(portfolio.keys())
create_widget()

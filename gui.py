import tkinter as tk
from tkinter import ttk, messagebox
from main import validate_ticker, call_option_price, put_option_price, get_market_data, get_historical_volatility

def calculate_price():
    """
    Fetches market data for the given ticker, calculates the option price,
    and updates the GUI with the result.
    """
    try:
        # Get user inputs from the GUI
        ticker = ticker_entry.get().upper()
        if not ticker:
            raise ValueError("Ticker symbol cannot be empty or invalid.")
        elif not validate_ticker(ticker):
            raise ValueError(f"Ticker symbol '{ticker}' is invalid or does not exist.")
        
        if (not strike_price_entry.get() or not time_to_expiry_entry.get()):
            raise ValueError("Strike price and time to expiry must be provided.")
        
        strike_price = float(strike_price_entry.get())
        time_to_expiry_days = float(time_to_expiry_entry.get())
        time_to_expiry = time_to_expiry_days / 365.0

        if (strike_price <= 0 or time_to_expiry <= 0):
            raise ValueError("Strike price and time to expiry must be positive numbers.")

        # Fetch market data using functions from main.py
        result_label.config(text="Fetching data...")
        root.update_idletasks() # Update GUI to show message

        stock_price, dividend_yield, risk_free_rate = get_market_data(ticker)
        volatility = get_historical_volatility(ticker)

        # Calculate the option prices
        call_price = call_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
    
        put_price = put_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
    
        # Display the result
        result_text = (
            f"Call Option Price: {call_price:.2f}\n\n"
            f"Put Option Price: {put_price:.2f}\n\n"
            f"Fetched Data:\n"
            f"  Stock Price: {stock_price:.2f}\n"
            f"  Volatility: {volatility*100:.2f}%\n"
            f"  Risk-Free Rate: {risk_free_rate*100:.2f}%\n"
            f"  Dividend Yield: {dividend_yield*100:.2f}%"
        )
        result_label.config(text=result_text)

    except ValueError as e:
        messagebox.showerror("Failed", e)
        result_label.config(text="Option Price: -")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        result_label.config(text="Option Price: -")

# --- GUI Setup ---
root = tk.Tk()
root.title("BSM Option Pricer")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# --- Input Fields and Labels ---
ttk.Label(frame, text="Stock Ticker:").grid(column=0, row=0, sticky=tk.W, pady=2)
ticker_entry = ttk.Entry(frame)
ticker_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=2)

ttk.Label(frame, text="Strike Price:").grid(column=0, row=1, sticky=tk.W, pady=2)
strike_price_entry = ttk.Entry(frame)
strike_price_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=2)

ttk.Label(frame, text="Time to Expiry (days):").grid(column=0, row=2, sticky=tk.W, pady=2)
time_to_expiry_entry = ttk.Entry(frame)
time_to_expiry_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=2)


# --- Buttons and Result ---
calculate_button = ttk.Button(frame, text="Calculate Price", command=calculate_price)
calculate_button.grid(column=0, row=4, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="Option Price: -", justify=tk.LEFT)
result_label.grid(column=0, row=5, columnspan=2, sticky=tk.W, pady=10)

# Make the columns in the frame responsive
frame.columnconfigure(1, weight=1)

# --- Run the application ---
root.mainloop()
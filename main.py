import math
import yfinance as yf
import numpy as np

def get_market_data(ticker_symbol):
    """Fetches current stock price, dividend yield, and risk-free rate for a given ticker."""
    ticker = yf.Ticker(ticker_symbol)
    
    # Get current stock price
    stock_price = ticker.history(period="1d")['Close'].iloc[-1]
    if not stock_price:
        raise ValueError(f"Could not fetch stock price for {ticker_symbol}")

    # Get dividend yield
    dividend_yield = ticker.info.get('dividendYield', 0.0)

    # Use the 13-week Treasury Bill yield (^IRX) as a proxy for the risk-free rate
    risk_free_rate_ticker = yf.Ticker("^IRX")
    risk_free_rate = risk_free_rate_ticker.history(period="1d")['Close'].iloc[-1] / 100.0

    return stock_price, dividend_yield, risk_free_rate

def validate_ticker(ticker_symbol):
    """Validates if the given ticker symbol exists."""
    ticker = yf.Ticker(ticker_symbol) 
    return(ticker.info['trailingPegRatio'] is not None)  # Debugging line to check ticker info

def get_historical_volatility(ticker_symbol, period="1y"):
    """Calculates the annualized historical volatility of a stock."""
    try:
        ticker = yf.Ticker(ticker_symbol)
    except Exception as e:
        print(f"Error fetching ticker data: {e}")
    hist = ticker.history(period=period)
    log_returns = np.log(hist['Close'] / hist['Close'].shift(1))
    # Annualize the standard deviation of log returns
    volatility = log_returns.std() * np.sqrt(252) 
    return volatility


def norm_cdf(x):
    """Calculates the cumulative distribution function for the standard normal distribution."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def as_decimal(x):
    """Converts a percentage to a decimal if it's >= 1."""
    return x / 100.0 if x >= 1 else x

def call_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield=0.0):
    """
    Calculates the Black-Scholes price for a European call option with a continuous dividend yield.
    """
    q = dividend_yield
    T = time_to_expiry
    S, K, r, sigma = stock_price, strike_price, risk_free_rate, volatility

    if T <= 0 or sigma <= 0:
        return max(0.0, S * math.exp(-q * T) - K * math.exp(-r * T))

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call_price = S * math.exp(-q * T) * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    return call_price

def call_with_discrete_dividends(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividends):
    """
    Calculates the Black-Scholes price for a European call option with discrete dividends.
    """
    T = time_to_expiry
    r = risk_free_rate
    pv_divs = sum(D * math.exp(-r * t) for D, t in dividends if 0 < t <= T)
    s_adj = max(1e-12, stock_price - pv_divs)
    return call_option_price(s_adj, strike_price, T, r, volatility, dividend_yield=0.0)

def put_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield=0.0):
    """
    Calculates the Black-Scholes price for a European put option with a continuous dividend yield.
    """
    q = dividend_yield
    T = time_to_expiry
    S, K, r, sigma = stock_price, strike_price, risk_free_rate, volatility

    if T <= 0 or sigma <= 0:
        return max(0.0, K * math.exp(-r * T) - S * math.exp(-q * T))

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    put_price = K * math.exp(-r * T) * norm_cdf(-d2) - S * math.exp(-q * T) * norm_cdf(-d1)
    return put_price

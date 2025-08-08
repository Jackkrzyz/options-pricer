import math

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def as_decimal(x):
    return x / 100.0 if x >= 1 else x

def call_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield=0.0):
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
    T = time_to_expiry
    r = risk_free_rate
    pv_divs = sum(D * math.exp(-r * t) for D, t in dividends if 0 < t <= T)
    s_adj = max(1e-12, stock_price - pv_divs)
    return call_option_price(s_adj, strike_price, T, r, volatility, dividend_yield=0.0)


def main():
    while True:
        print("BSM Option Pricer")
        stock_price  = float(input("Stock Price: "))
        strike_price = float(input("Strike Price: "))
        time_to_expiry = float(input("Time to Expiry (in years): "))
        risk_free_rate = as_decimal(float(input("Risk-Free Rate (% or decimal): ")))
        volatility = as_decimal(float(input("Volatility (% or decimal): ")))
        dividend_yield = as_decimal(float(input("Dividend Yield (% or decimal, 0 if none): ")))
        if dividend_yield is not 0:
            are_dividends_discrete = input("Are Dividends Discrete? (yes/no): ").strip().lower()
            if are_dividends_discrete == 'yes':
                dividends = []
                while True:
                    dividend_input = input("Enter dividend amount and time to payment (e.g. '1.00 0.5') or 'done' to finish: ")
                    if dividend_input.lower() == 'done':
                        break
                    try:
                        D, t = map(float, dividend_input.split())
                        dividends.append((D, t))
                    except ValueError:
                        print("Invalid input. Please enter in the format 'amount time'.")
            option_type = input("Option Type (Call/Put): ").strip().lower()

        

        if option_type == 'call':
            if are_dividends_discrete == 'yes':
                price = call_with_discrete_dividends(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividends)
            else:
                price = call_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
            input(f"Call Option Price: {price:.2f}")
        else:
            print("Put option pricing is not implemented in this version.")

if __name__ == "__main__":
    main()
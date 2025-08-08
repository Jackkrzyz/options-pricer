import math

def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

def as_decimal(x):
    return x / 100.0 if x > 1 else x

def call_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield=0):
    q = dividend_yield
    if q > 0:
        d1 = (math.log(stock_price / strike_price) + (risk_free_rate - q + 0.5 * volatility ** 2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    else:
        d1 = (math.log(stock_price / strike_price) + (risk_free_rate + volatility ** 2 / 2) * time_to_expiry) / (volatility * math.sqrt(time_to_expiry))
    d2 = d1 - volatility * math.sqrt(time_to_expiry)
    call_price = stock_price * norm_cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm_cdf(d2)
    return call_price



def main():
    print("BSM Option Pricer")
    stock_price  = float(input("Stock Price: "))
    strike_price = float(input("Strike Price: "))
    time_to_expiry = float(input("Time to Expiry (in years): "))
    risk_free_rate = as_decimal(float(input("Risk-Free Rate: ")))
    volatility = as_decimal(float(input("Volatility: ")))
    option_type = input("Option Type (Call/Put): ").strip().lower()
    dividend_yield = as_decimal(float(input("Dividend Yield (% or decimal, 0 if none): ")))
    

    if option_type == 'call':
        price = call_option_price(stock_price, strike_price, time_to_expiry, risk_free_rate, volatility, dividend_yield)
        print(f"Call Option Price: {price:.2f}")
    else:
        print("Put option pricing is not implemented in this version.")

if __name__ == "__main__":
    main()
import numpy as np
import matplotlib.pyplot as plt
import src.models as models
import src.strategies as strategies

# --------------------------------------

# Parameters
initial_mortgage = 4100000  # SEK
exogenous_cash_inflow = 17000  # SEK per month

# Vasicek Model for interest rates
annual_mean_interest_rate = 0.03  # Long-term mean rate
interest_rate_volatility = 0.0111  # Annual volatility
interest_rate_speed = 0.1  # Speed of reversion

# GBM for stock returns
annual_stock_return = 0.08
stock_return_volatility = 0.20

print("Strategy 1: Pay extra towards mortgage")

# Initialize models for Strategy 1
interest_rate_model1 = models.InterestRateModel(
    initial_rate=annual_mean_interest_rate,
    mean_rate=annual_mean_interest_rate,
    speed_of_reversion=interest_rate_speed,
    volatility=interest_rate_volatility
)

stock_model1 = models.StockModel(
    initial_value=0,
    expected_return=annual_stock_return,
    volatility=stock_return_volatility
)

model1 = models.CashFlowModel(
    initial_mortgage=initial_mortgage,
    exogenous_cash_inflow=exogenous_cash_inflow,
    interest_rate_model=interest_rate_model1,
    stock_model=stock_model1,
    initial_cash=0  # Assuming no initial cash
)

strategy1 = strategies.MortgageFocusStrategy()

# Simulate for 12 months
for month in range(12):
    model1.simulate_month(strategy1)

model1.print_cash_flow_history()
# plot the cash flow history
cash_flow_history = model1.cash_flow_history
months = [cf['month'] for cf in cash_flow_history]
total_pnl = [cf['total_pnl'] for cf in cash_flow_history]
interest_payment = [cf['interest_payment'] for cf in cash_flow_history]
mandatory_down_payment = [cf['mandatory_down_payment'] for cf in cash_flow_history]
extra_mortgage_payment = [cf['extra_mortgage_payment'] for cf in cash_flow_history]
investment_investment = [cf['investment_investment'] for cf in cash_flow_history]
investment_return = [cf['investment_return'] for cf in cash_flow_history]
# pyplot
plt.figure(figsize=(12, 6))
plt.plot(months, total_pnl, label='Total P&L')
plt.plot(months, interest_payment, label='Interest Payment')
plt.plot(months, mandatory_down_payment, label='Mandatory Down Payment')
plt.plot(months, extra_mortgage_payment, label='Extra Mortgage Payment')
plt.plot(months, investment_investment, label='Investment in Portfolio')
plt.plot(months, investment_return, label='Investment Return')
plt.legend()
plt.xlabel('Months')
plt.ylabel('Amount (SEK)')
plt.title('Cash Flow Components Over 12 Months')
plt.grid(True)
plt.show()



print("\nStrategy 2: Invest in stock market")

# Initialize models for Strategy 2
interest_rate_model2 = models.InterestRateModel(
    initial_rate=annual_mean_interest_rate,
    mean_rate=annual_mean_interest_rate,
    speed_of_reversion=interest_rate_speed,
    volatility=interest_rate_volatility
)

stock_model2 = models.StockModel(
    initial_value=0,
    expected_return=annual_stock_return,
    volatility=stock_return_volatility
)

model2 = models.CashFlowModel(
    initial_mortgage=initial_mortgage,
    exogenous_cash_inflow=exogenous_cash_inflow,
    interest_rate_model=interest_rate_model2,
    stock_model=stock_model2,
    initial_cash=0  # Assuming no initial cash
)

strategy2 = strategies.InvestmentFocusStrategy()

# Simulate for 12 months
for month in range(12):
    model2.simulate_month(strategy2)

model2.print_cash_flow_history()
# plot the cash flow history
cash_flow_history = model2.cash_flow_history
months = [cf['month'] for cf in cash_flow_history]
total_pnl = [cf['total_pnl'] for cf in cash_flow_history]
interest_payment = [cf['interest_payment'] for cf in cash_flow_history]
mandatory_down_payment = [cf['mandatory_down_payment'] for cf in cash_flow_history]
extra_mortgage_payment = [cf['extra_mortgage_payment'] for cf in cash_flow_history]
investment_investment = [cf['investment_investment'] for cf in cash_flow_history]
investment_return = [cf['investment_return'] for cf in cash_flow_history]
# pyplot
plt.figure(figsize=(12, 6))
plt.plot(months, total_pnl, label='Total P&L')
plt.plot(months, interest_payment, label='Interest Payment')
plt.plot(months, mandatory_down_payment, label='Mandatory Down Payment')
plt.plot(months, extra_mortgage_payment, label='Extra Mortgage Payment')
plt.plot(months, investment_investment, label='Investment in Portfolio')
plt.plot(months, investment_return, label='Investment Return')
plt.legend()
plt.xlabel('Months')
plt.ylabel('Amount (SEK)')
plt.title('Cash Flow Components Over 12 Months')
plt.grid(True)
plt.show()

# print the final cumulative pnl for each strategy
print("Strategy 1 Total P&L:", model1.total_equity())
print("Strategy 2 Total P&L:", model2.total_equity())

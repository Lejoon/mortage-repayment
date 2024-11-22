import numpy as np
import matplotlib.pyplot as plt
import src.models as models
import src.strategies as strategies
import copy  # Added import for deep copying

class SimulatedCashFlowModel(models.CashFlowModel):
    def __init__(self, *args, inflation_rate=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.inflation_rate = inflation_rate
        self.base_cash_inflow = self.exogenous_cash_inflow

    def simulate_month(self, strategy):
        # Update cash inflow with inflation
        self.exogenous_cash_inflow = self.base_cash_inflow * (1 + self.inflation_rate/12) ** self.current_time

        # Initialize P&L for the period
        pnl = 0

        # Cash flow dictionary for the current month
        cash_flows = {
            'month': self.current_time,
            'exogenous_cash_inflow': self.exogenous_cash_inflow,
            'interest_payment': 0,
            'mandatory_down_payment': 0,
            'extra_mortgage_payment': 0,
            'investment_investment': 0,
            'investment_return': 0,
            'interest_rate': self.interest_rate_model.current_rate,
            'total_pnl': 0
        }

        # 1. Exogenous cash inflow (Income)
        self.assets['cash'] += self.exogenous_cash_inflow
        pnl += self.exogenous_cash_inflow
        cash_flows['exogenous_cash_inflow'] = self.exogenous_cash_inflow

        # 2. Interest rate payment (Expense)
        interest_payment = self.liabilities['mortgage'] * self.interest_rate_model.current_rate / 12
        self.assets['cash'] -= interest_payment
        pnl -= interest_payment
        cash_flows['interest_payment'] = -interest_payment

        # Get allocations from strategy
        allocations = strategy.allocate_cash_flow(self)
        mandatory_down_payment = allocations.get('mandatory_down_payment', 0)
        extra_mortgage_payment = allocations.get('extra_mortgage_payment', 0)
        investment_investment = allocations.get('investment_investment', 0)

        cash_flows['mandatory_down_payment'] = mandatory_down_payment
        cash_flows['extra_mortgage_payment'] = extra_mortgage_payment
        cash_flows['investment_investment'] = investment_investment

        # Principal repayments (Balance Sheet Movements)
        total_mortgage_payment = mandatory_down_payment + extra_mortgage_payment
        self.liabilities['mortgage'] -= total_mortgage_payment
        self.assets['cash'] -= total_mortgage_payment

        # Investment in portfolio (Asset Transfer)
        self.assets['cash'] -= investment_investment

        # 3. Simulate the return on the investment portfolio
        previous_investment_value = self.assets['investment_portfolio']
        new_investment_value = self.stock_model.simulate_next(delta_t=1/12, investment=investment_investment)
        investment_return = new_investment_value - previous_investment_value - investment_investment

        # Update the investment portfolio value in assets
        self.assets['investment_portfolio'] = new_investment_value
        cash_flows['investment_return'] = investment_return

        # Include investment return in P&L
        pnl += investment_return

        # 4. Update retained earnings after all P&L items
        self.equity['retained_earnings'] += pnl
        cash_flows['total_pnl'] = pnl

        # Simulate the interest rate for the next period
        new_interest_rate = self.interest_rate_model.simulate_next(delta_t=1/12)
        cash_flows['new_interest_rate'] = new_interest_rate

        # Append the cash flow to history
        self.cash_flow_history.append(cash_flows)

        # Check balance sheet
        self.check_balance_sheet()

        # Move to the next month
        self.current_time += 1

# Parameters
initial_mortgage = 4100000  # SEK
exogenous_cash_inflow = 17000  # SEK per month
inflation_rate = 0.02  # 2% annual inflation

# Vasicek Model for interest rates
annual_mean_interest_rate = 0.03  # Long-term mean rate
interest_rate_volatility = 0.0111  # Annual volatility
interest_rate_speed = 0.1  # Speed of reversion

# GBM for stock returns
annual_stock_return = 0.08
stock_return_volatility = 0.20

# Simulation
months = 5*12  # 5 years
simulations = 10000

# Store histories for plotting
simulation_histories = []

for simulation in range(simulations):
    # Initialize models with the RNG
    interest_rate_model = models.InterestRateModel(
        initial_rate=annual_mean_interest_rate,
        mean_rate=annual_mean_interest_rate,
        speed_of_reversion=interest_rate_speed,
        volatility=interest_rate_volatility
    )

    stock_model = models.StockModel(
        initial_value=0,
        expected_return=annual_stock_return,
        volatility=stock_return_volatility
    )

    model = SimulatedCashFlowModel(
        initial_mortgage=initial_mortgage,
        exogenous_cash_inflow=exogenous_cash_inflow,
        interest_rate_model=interest_rate_model,
        stock_model=stock_model,
        initial_cash=0,
        inflation_rate=inflation_rate
    )

    strategy = strategies.InvestmentFocusStrategy()

    # Simulate for 5 years
    for month in range(months):
        model.simulate_month(strategy)

    # Store the final equity
    if simulation == 0:
        equity = model.total_equity()
    else:
        equity = np.vstack((equity, model.total_equity()))
    
    # Store this simulation's history
    simulation_histories.append(copy.deepcopy(model.cash_flow_history))

# --------------------
# Plots and Statistics
# --------------------

# Plot the cumulative equity paths
plt.figure(figsize=(10, 6))
for i in range(min(1000, simulations)):  # Plot only the first 100 simulations for clarity
    cumulative_equity = [cf['total_pnl'] for cf in simulation_histories[i]]
    plt.plot(np.cumsum(cumulative_equity), label=f'Simulation {i+1}', alpha=0.3)

plt.xlabel('Months')
plt.ylabel('Cumulative Equity')
plt.title('Simulated Cumulative Equity Paths')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.tight_layout()
plt.show()

# Convert to a NumPy array for easier manipulation
final_equity_values = np.array(equity)

# Plot the distribution of the final equity values
plt.figure(figsize=(10, 6))
plt.hist(final_equity_values, bins=30, alpha=0.7, color='blue', edgecolor='black')
plt.xlabel('Final Equity')
plt.ylabel('Frequency')
plt.title('Distribution of Final Equity Values')
plt.grid(True)
plt.tight_layout()
plt.show()

# Calculate the mean and standard deviation of the final equity
mean_equity = np.mean(equity)
std_equity = np.std(equity)

print("Mean Equity:", mean_equity)
print("Std Equity:", std_equity)

# Calculate VaR at the 5th percentile
var_5th_percentile = np.percentile(final_equity_values, 5)
print("VaR at 5th Percentile:", var_5th_percentile)

num_scenarios_negative_equity = np.sum(final_equity_values < 0)/simulations
print("Number of scenarios with equity < 0:", num_scenarios_negative_equity)

import numpy as np
class InterestRateModel:
    def __init__(self, initial_rate, mean_rate, speed_of_reversion, volatility):
        self.current_rate = initial_rate
        self.mean_rate = mean_rate
        self.speed_of_reversion = speed_of_reversion  # 'a' parameter
        self.volatility = volatility  # 'sigma' parameter

    def simulate_next(self, delta_t=1/12):
        """
        Simulate the next interest rate using the exact discretization of the Vasicek model.

        Parameters:
            delta_t (float): Time step in years (e.g., 1/12 for monthly steps)

        Returns:
            float: The next interest rate
        """
        a = self.speed_of_reversion
        b = self.mean_rate
        sigma = self.volatility
        r_t = self.current_rate

        # Exact discretization
        epsilon = np.random.normal()
        exponent = -a * delta_t
        mean = b + (r_t - b) * np.exp(exponent)
        variance = (sigma**2 / (2 * a)) * (1 - np.exp(2 * exponent))
        std_dev = np.sqrt(variance)
        r_t_plus_dt = mean + std_dev * epsilon

        # Apply floor to prevent negative interest rates
        r_t_plus_dt = max(r_t_plus_dt, 0)

        self.current_rate = r_t_plus_dt
        return self.current_rate

class StockModel:
    def __init__(self, initial_value, expected_return, volatility):
        self.current_value = initial_value
        self.expected_return = expected_return  # 'mu' parameter
        self.volatility = volatility  # 'sigma' parameter

    def simulate_next(self, delta_t=1/12, investment=0):
        """
        Simulate the next value of the investment portfolio using GBM.

        Parameters:
            delta_t (float): Time step in years (e.g., 1/12 for monthly steps)
            investment (float): Additional investment added to the portfolio at the beginning of the period

        Returns:
            float: The next value of the investment portfolio
        """
        mu = self.expected_return
        sigma = self.volatility

        # If current_value is zero and investment is zero, return zero
        if self.current_value == 0 and investment == 0:
            return 0

        # Add investment at the beginning
        S_t = self.current_value + investment

        # Simulate growth
        epsilon = np.random.normal()
        growth_factor = np.exp((mu - 0.5 * sigma**2) * delta_t + sigma * np.sqrt(delta_t) * epsilon)
        S_t_plus_dt = S_t * growth_factor

        # Update current value
        self.current_value = S_t_plus_dt
        return self.current_value


class CashFlowModel:
    def __init__(self, initial_mortgage, exogenous_cash_inflow,
                 interest_rate_model, stock_model, initial_cash=0):

        # Parameters
        self.initial_mortgage = initial_mortgage
        self.exogenous_cash_inflow = exogenous_cash_inflow

        # Models
        self.interest_rate_model = interest_rate_model
        self.stock_model = stock_model

        # Initialize the balance sheet
        self.assets = {
            'residency': self.initial_mortgage,  # Asset corresponding to the mortgage
            'investment_portfolio': 0,           # Starts with 0
            'cash': initial_cash                 # Cash in equity
        }

        self.liabilities = {
            'mortgage': self.initial_mortgage    # Mortgage liability
        }

        # Equity includes initial cash contribution
        self.equity = {
            'initial_contribution': initial_cash,
            'retained_earnings': 0               # Equity starts at 0
        }

        # Time tracking
        self.current_time = 0  # Start at time 0 (month 0)
        self.cash_flow_history = []  # List to keep track of all cash flows

    def total_assets(self):
        return sum(self.assets.values())

    def total_liabilities(self):
        return sum(self.liabilities.values())

    def total_equity(self):
        return sum(self.equity.values())

    def check_balance_sheet(self):
        assets_total = self.total_assets()
        liabilities_total = self.total_liabilities()
        equity_total = self.total_equity()
        assert abs(assets_total - (liabilities_total + equity_total)) < 1e-6, \
            f"Balance sheet does not balance: Assets ({assets_total}) != Liabilities ({liabilities_total}) + Equity ({equity_total})"

    def simulate_month(self, strategy):
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

        # Now, after paying interest, call strategy to allocate remaining cash
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

        # 3. Simulate the return on the investment portfolio, including the new investment
        previous_investment_value = self.assets['investment_portfolio']
        new_investment_value = self.stock_model.simulate_next(delta_t=1/12, investment=investment_investment)

        # Investment return is the growth over the period
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

        # Append the cash flow of the current month to the history
        self.cash_flow_history.append(cash_flows)

        # Check balance sheet
        self.check_balance_sheet()

        # Move to the next month
        self.current_time += 1


    # Method to print the cash flow history
    def print_cash_flow_history(self):
        print("Cash Flow History:")
        for cash_flow in self.cash_flow_history:
            print(cash_flow)


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
                 interest_rate_model, stock_model, initial_cash=0, inflation_rate=0.02):

        # Parameters
        self.initial_mortgage = initial_mortgage
        self.base_cash_inflow = exogenous_cash_inflow
        self.exogenous_cash_inflow = exogenous_cash_inflow
        self.inflation_rate = inflation_rate

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
        """
        Placeholder method that should be implemented by subclasses or overridden at instance creation.
        
        Parameters:
            strategy: Strategy object that determines cash flow allocation
        """
        raise NotImplementedError("simulate_month must be implemented")

    # Method to print the cash flow history
    def print_cash_flow_history(self):
        print("Cash Flow History:")
        for cash_flow in self.cash_flow_history:
            print(cash_flow)


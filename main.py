import numpy as np
import matplotlib.pyplot as plt
from src.simulation import run_simulation

months = 10 * 12
simulations = 10000

def main():
    # Parameters
    initial_mortgage = 4100000  # SEK
    monthly_cash = 17000  # SEK

    # Vasicek Model for interest rates
    annual_mean_interest_rate = 0.03  # Long-term mean rate
    interest_rate_volatility = 0.0111  # Annual volatility
    interest_rate_speed = 0.1  # Speed of reversion

    # GBM for stock returns
    annual_stock_return = 0.08
    stock_return_volatility = 0.20

 
    #number of bins historgram based on sqrt of simulations
    n_bins = int(np.sqrt(simulations))

    # Run the simulation
    results = run_simulation(
        initial_mortgage,
        monthly_cash,
        annual_mean_interest_rate,
        interest_rate_volatility,
        interest_rate_speed,
        annual_stock_return,
        stock_return_volatility,
        months,
        simulations
    )

    # Unpack results
    (mortgage_balances_strategy1,
     mortgage_balances_strategy2,
     cumulative_paydown_strategy1,
     final_portfolio_values,
     total_cash_spent_strategy1,
     total_cash_spent_strategy2) = results

    # Generate plots
    generate_plots(
        mortgage_balances_strategy1,
        mortgage_balances_strategy2,
        cumulative_paydown_strategy1,
        final_portfolio_values,
        n_bins
    )

    # Display expected values
    display_expected_values(
        mortgage_balances_strategy1,
        mortgage_balances_strategy2,
        cumulative_paydown_strategy1,
        final_portfolio_values
    )

    # Display total cash spent
    print('Total cash spent (Strategy 1):', np.mean(total_cash_spent_strategy1))
    print('Total cash spent (Strategy 2):', np.mean(total_cash_spent_strategy2))

def generate_plots(mbs1, mbs2, cps1, fpv, n_bins):
    # Plot histograms of final mortgage balances
    plt.figure(figsize=(10, 6))
    bins = np.linspace(min(np.min(mbs1), np.min(mbs2)), max(np.max(mbs1), np.max(mbs2)), n_bins)
    plt.hist(mbs1, bins=bins, alpha=0.5, label='Pay Down Mortgage')
    plt.hist(mbs2, bins=bins, alpha=0.5, label='Invest in Stocks')
    plt.xlabel('Final Mortgage Balance (SEK)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title('Expected Mortgage Balances After 5 Years')
    plt.savefig('plots/mortgage_balances.png')
    plt.show()

    # Plot histogram of final portfolio values
    plt.figure(figsize=(10, 6))
    bins = np.linspace(min(np.min(cps1), np.min(fpv)), max(np.max(cps1), np.max(fpv)), n_bins)
    plt.hist(cps1, bins=bins, alpha=0.7, color='blue', label='Pay Down Mortgage')
    plt.hist(fpv, bins=bins, alpha=0.7, color='green', label='Invest in Stocks')
    plt.xlabel('Final Portfolio Value (SEK)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Final Portfolio Values')
    plt.legend()
    plt.savefig('plots/portfolio_values.png')
    plt.show()

def display_expected_values(mbs1, mbs2, cps1, fpv):
    mean_balance_strategy1 = np.mean(mbs1)
    mean_balance_strategy2 = np.mean(mbs2)
    mean_paydown_strategy1 = np.mean(cps1)
    mean_portfolio_value = np.mean(fpv)

    print('Expected final mortgage balance (Strategy 1):', mean_balance_strategy1)
    print('Expected final mortgage balance (Strategy 2):', mean_balance_strategy2)
    print('Expected total cumulative paydown (Strategy 1):', mean_paydown_strategy1)
    print('Expected final portfolio value (Strategy 2):', mean_portfolio_value)

if __name__ == '__main__':
    main()

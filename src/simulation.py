import numpy as np

def run_simulation(
    initial_mortgage,
    monthly_cash,
    annual_mean_interest_rate,
    interest_rate_volatility,
    interest_rate_speed,
    annual_stock_return,
    stock_return_volatility,
    months,
    simulations
):
    # Lists to store final values
    mortgage_balances_strategy1 = []
    mortgage_balances_strategy2 = []
    cumulative_paydown_strategy1 = []
    final_portfolio_values = []
    total_cash_spent_strategy1 = []
    total_cash_spent_strategy2 = []

    dt = 1 / 12  # Monthly time step

    for _ in range(simulations):
        (mortgage_balance1,
         mortgage_balance2,
         cumulative_paydown,
         investment_portfolio,
         cash_spent1,
         cash_spent2) = simulate_single_path(
            initial_mortgage,
            monthly_cash,
            annual_mean_interest_rate,
            interest_rate_volatility,
            interest_rate_speed,
            annual_stock_return,
            stock_return_volatility,
            months,
            dt
        )

        # Store results
        mortgage_balances_strategy1.append(mortgage_balance1)
        mortgage_balances_strategy2.append(mortgage_balance2)
        cumulative_paydown_strategy1.append(cumulative_paydown)
        final_portfolio_values.append(investment_portfolio)
        total_cash_spent_strategy1.append(cash_spent1)
        total_cash_spent_strategy2.append(cash_spent2)

    return (
        mortgage_balances_strategy1,
        mortgage_balances_strategy2,
        cumulative_paydown_strategy1,
        final_portfolio_values,
        total_cash_spent_strategy1,
        total_cash_spent_strategy2
    )

def simulate_single_path(
    initial_mortgage,
    monthly_cash,
    annual_mean_interest_rate,
    interest_rate_volatility,
    interest_rate_speed,
    annual_stock_return,
    stock_return_volatility,
    months,
    dt
):
    mortgage_balance1 = initial_mortgage
    mortgage_balance2 = initial_mortgage
    investment_portfolio = 0
    cumulative_paydown = 0
    total_cash_spent_strategy1 = 0
    total_cash_spent_strategy2 = 0
    r_t = annual_mean_interest_rate / 12  # Initial monthly interest rate

    # Generate random shocks
    interest_rate_dW = np.random.normal(0, np.sqrt(dt), months)
    stock_return_epsilon = np.random.normal(0, 1, months)

    for t in range(months):
        # Vasicek model for interest rate
        dr_t = interest_rate_speed * (annual_mean_interest_rate / 12 - r_t) * dt \
               + interest_rate_volatility * interest_rate_dW[t]
        r_t += dr_t
        r_t = max(r_t, 0)  # Ensure non-negative interest rate

        # Interest payments for both strategies
        interest_payment1 = mortgage_balance1 * r_t
        interest_payment2 = mortgage_balance2 * r_t

        # Required monthly principal payment (1%/12 of current balance)
        required_principal1 = mortgage_balance1 * 0.01 / 12
        required_principal2 = mortgage_balance2 * 0.01 / 12

        # Remaining cash after paying interest
        remaining_cash1 = monthly_cash - interest_payment1
        remaining_cash2 = monthly_cash - interest_payment2

        # Ensure remaining cash isn't negative
        remaining_cash1 = max(remaining_cash1, 0)
        remaining_cash2 = max(remaining_cash2, 0)

        # Strategy 1: Pay required principal plus any extra
        principal_payment1 = min(remaining_cash1, mortgage_balance1)
        mortgage_balance1 -= principal_payment1
        cumulative_paydown += principal_payment1
        total_cash_spent_strategy1 += interest_payment1 + principal_payment1

        # Strategy 2: Pay minimum required principal, invest the rest
        principal_payment2 = min(required_principal2, remaining_cash2)
        mortgage_balance2 -= principal_payment2
        total_cash_spent_strategy2 += interest_payment2 + principal_payment2
        
        # Invest remaining cash after minimum payment
        investment_cash = remaining_cash2 - principal_payment2
        
        # Simulate stock return with GBM
        monthly_return = np.exp(
            (annual_stock_return - 0.5 * stock_return_volatility ** 2) * dt +
            stock_return_volatility * np.sqrt(dt) * stock_return_epsilon[t]
        ) - 1
        investment_portfolio = investment_portfolio * (1 + monthly_return) + investment_cash

        # Ensure non-negative balances
        mortgage_balance1 = max(mortgage_balance1, 0)
        mortgage_balance2 = max(mortgage_balance2, 0)

    # Pay off mortgage with investment portfolio at the end
    mortgage_balance2 -= investment_portfolio
    mortgage_balance2 = max(mortgage_balance2, 0)

    return mortgage_balance1, mortgage_balance2, cumulative_paydown, investment_portfolio, total_cash_spent_strategy1, total_cash_spent_strategy2

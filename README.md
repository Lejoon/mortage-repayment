# Mortgage Repayment Strategies Simulation

This project simulates two mortgage repayment strategies over a period of 5 years using Monte Carlo methods:

1. **Paying down the mortgage principal** with available monthly cash.
2. **Investing the available monthly cash in stocks** and using the investment portfolio to pay off the mortgage at the end.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Simulation Details](#simulation-details)
- [Results](#results)
- [License](#license)

## Project Overview

The simulation compares the effectiveness of two strategies in managing mortgage repayment by considering variables such as interest rates and stock market returns, both modeled using stochastic processes.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/mortgage_simulation_project.git
   ```

2. **Navigate to the project directory:**
   ```
   cd mortgage_simulation_project
   ```

3. **Create a virtual environment (optional but recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

4. **Install the required packages:**

```bash
pip install -r requirements.txt
```

## Usage

Run the simulation by executing:

```bash
python main.py
```

The results, including plots and expected values, will be displayed and saved in the plots/ directory.

## Simulation Details

    Interest Rate Modeling: The Vasicek model is used to simulate stochastic interest rates.
    Stock Returns Modeling: Geometric Brownian Motion (GBM) models the stock returns.
    Monte Carlo Simulations: The simulation runs multiple iterations (default 1000) to estimate the distributions.

## Parameters

    Initial Mortgage: 2,000,000 SEK
    Monthly Cash Available: 10,000 SEK
    Simulation Period: 5 years (60 months)
    Number of Simulations: 1000

## Results

The simulation generates histograms of final mortgage balances and investment portfolio values, along with expected (mean) values for each strategy.

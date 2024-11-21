

class Strategy:
    def allocate_cash_flow(self, model):
        """
        Determines how to allocate the available cash after interest payment.
        Should return a dictionary with keys:
            'mandatory_down_payment'
            'extra_mortgage_payment'
            'investment_investment'
        """
        raise NotImplementedError("This method should be overridden by subclasses")

class MortgageFocusStrategy(Strategy):
    def allocate_cash_flow(self, model):
        available_cash = model.assets['cash']

        # Calculate mandatory down payment as 1% annual of the mortgage balance per month
        mandatory_down_payment = model.liabilities['mortgage'] * (0.01 / 12)

        # Ensure we have enough cash to cover the mandatory down payment
        if available_cash < mandatory_down_payment:
            # Not enough cash to cover mandatory down payment
            mandatory_down_payment = available_cash
            extra_mortgage_payment = 0
            investment_investment = 0
        else:
            available_cash -= mandatory_down_payment

            # All remaining cash goes to extra mortgage payment
            extra_mortgage_payment = available_cash
            investment_investment = 0

        return {
            'mandatory_down_payment': mandatory_down_payment,
            'extra_mortgage_payment': extra_mortgage_payment,
            'investment_investment': investment_investment
        }

class InvestmentFocusStrategy(Strategy):
    def allocate_cash_flow(self, model):
        available_cash = model.assets['cash']

        # Calculate mandatory down payment as 1% annual of the mortgage balance per month
        mandatory_down_payment = model.liabilities['mortgage'] * (0.01 / 12)

        # Ensure we have enough cash to cover the mandatory down payment
        if available_cash < mandatory_down_payment:
            # Not enough cash to cover mandatory down payment
            mandatory_down_payment = available_cash
            extra_mortgage_payment = 0
            investment_investment = 0
        else:
            available_cash -= mandatory_down_payment

            # All remaining cash goes to investment
            extra_mortgage_payment = 0
            investment_investment = available_cash

        return {
            'mandatory_down_payment': mandatory_down_payment,
            'extra_mortgage_payment': extra_mortgage_payment,
            'investment_investment': investment_investment
        }

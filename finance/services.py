def calculate_emi(principal, rate, months):
    r = rate / (12 * 100)
    emi = (principal * r * (1 + r) ** months) / ((1 + r) ** months - 1)
    return round(emi, 2)

def calculate_emi_breakdown(principal, rate, months):
    """
    Calculate month-wise EMI breakdown showing principal, interest, and remaining balance
    """
    r = rate / (12 * 100)  # Monthly interest rate
    emi = calculate_emi(principal, rate, months)

    breakdown = []
    remaining_balance = principal

    for month in range(1, months + 1):
        # Interest for this month
        interest_payment = remaining_balance * r

        # Principal for this month
        principal_payment = emi - interest_payment

        # Update remaining balance
        remaining_balance -= principal_payment

        # Ensure remaining balance doesn't go negative due to rounding
        if remaining_balance < 0:
            remaining_balance = 0
            principal_payment = emi - interest_payment

        breakdown.append({
            'month': month,
            'emi': round(emi, 2),
            'principal_payment': round(principal_payment, 2),
            'interest_payment': round(interest_payment, 2),
            'remaining_balance': round(remaining_balance, 2)
        })

    return breakdown

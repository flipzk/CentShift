def calculate_allocation(salary: float, strategy: str):
    """
    Calculates salary allocation based on a selected strategy.
    Returns a dictionary with categories and allocated values.
    """
    allocations = {}
    
    if strategy == "50/30/20":
        allocations = {
            "Expenses (Necessities)": salary * 0.50,
            "Investments": salary * 0.30,
            "Personal (Wants)": salary * 0.20
        }
    elif strategy == "Smart Saver (50/30/10/10)":
        allocations = {
            "Expenses (Necessities)": salary * 0.50,
            "Investments (Long Term)": salary * 0.30,
            "Personal (Wants)": salary * 0.10,
            "Savings (Emergency Fund)": salary * 0.10
        }
    elif strategy == "70/20/10":
        allocations = {
            "Expenses (Necessities)": salary * 0.70,
            "Personal (Wants)": salary * 0.20,
            "Savings/Investments": salary * 0.10
        }
    elif strategy == "Aggressive Investor (30/30/40)":
        allocations = {
            "Expenses (Necessities)": salary * 0.30,
            "Personal (Wants)": salary * 0.30,
            "Investments": salary * 0.40
        }
    else:
        allocations = {"Unallocated": salary}

    return allocations
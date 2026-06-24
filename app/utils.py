def calculate_score(total_amount, total_transactions):
    return round(
        (float(total_amount) * 0.6)
        + (total_transactions * 20),
        2
    )
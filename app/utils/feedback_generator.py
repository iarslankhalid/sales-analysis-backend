def generate_feedback(data):
    sales = data["sales"]
    if sales > 100000:
        return f"Excellent performance with sales of {sales}."
    return f"Needs improvement, sales achieved: {sales}."

def generate_team_feedback(team_data):
    total_sales = sum(rep["sales"] for rep in team_data)
    return f"The team achieved total sales of {total_sales}."

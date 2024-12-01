import pandas as pd
from collections import OrderedDict
from datetime import datetime
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()

def extract_employee_data(sales_data: pd.DataFrame, employee_id: int) -> dict:
    """
    Extract performance data for a specific sales representative.

    :param sales_data: A pandas DataFrame containing sales performance data.
    :param employee_id: The ID of the employee whose performance needs to be analyzed.
    :return: A dictionary containing the extracted performance metrics.
    """

    # Filter the data for the specific employee
    employee_data = sales_data[sales_data["employee_id"] == employee_id]

    if employee_data.empty:
        return f"No data found for employee with ID # {employee_id}. Try any of these IDs:\n {sales_data['employee_id'].unique()}"

    # Aggregate metrics for the sales representative
    employee_name = employee_data["employee_name"].iloc[0]
    total_sales = employee_data["revenue_confirmed"].sum()
    conversion_rate = employee_data["avg_close_rate_30_days"].mean()
    deals_closed = employee_data["tours_booked"].sum()
    recurring_sales = employee_data["revenue_pending"].sum()
    retention_rate = (employee_data["tours_scheduled"].sum() / employee_data["tours"].sum() * 100
                      if employee_data["tours"].sum() > 0 else 0)

    # Create a dictionary with the extracted metrics
    performance_data = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "total_sales": f"${total_sales}",
        "conversion_rate": f"{round(conversion_rate, 2)}%",
        "deals_closed": int(deals_closed),
        "recurring_sales": recurring_sales,
        "customer_retention_rate": f"{round(retention_rate, 2)}%"
    }

    return performance_data


def extract_team_data(sales_data: pd.DataFrame) -> dict:
    """
    Extract team performance metrics from a sales performance dataset.

    :param sales_data: A pandas DataFrame containing sales performance data.
    :return: A dictionary containing team performance metrics.
    """
    # Ensure relevant columns are numeric for calculations
    columns_to_numeric = [
        "revenue_confirmed", "avg_close_rate_30_days", "tours_booked",
        "revenue_pending", "tours_in_pipeline"
    ]
    sales_data[columns_to_numeric] = sales_data[columns_to_numeric].apply(pd.to_numeric, errors="coerce")

    # Handle empty or invalid datasets
    if sales_data.empty or sales_data["revenue_confirmed"].isna().all():
        raise ValueError("The dataset is empty or contains invalid revenue data.")

    # Calculate metrics
    total_sales = sales_data["revenue_confirmed"].sum()
    conversion_rate = sales_data["avg_close_rate_30_days"].mean()
    deals_closed = sales_data["tours_booked"].sum()
    total_tours_pipeline = sales_data["tours_in_pipeline"].sum()
    total_revenue_pending = sales_data["revenue_pending"].sum()
    avg_revenue_per_deal = total_sales / deals_closed if deals_closed > 0 else 0

    # Identify Top Performer
    top_performer_row = sales_data.loc[sales_data["revenue_confirmed"].idxmax()]
    top_performer = {
        "employee_id": int(top_performer_row["employee_id"]),
        "employee_name": top_performer_row["employee_name"],
        "revenue_confirmed": float(top_performer_row["revenue_confirmed"]),
    }

    # Build output dictionary
    output = {
        "total_sales": f"${total_sales}",
        "conversion_rate": f"{round(conversion_rate, 2)}%",
        "deals_closed": int(deals_closed),
        "average_revenue_per_deal": f"${round(avg_revenue_per_deal, 2)}",
        "total_tours_in_pipeline": int(total_tours_pipeline),
        "total_revenue_pending": f"${total_revenue_pending}",
        "top_performer": top_performer,
    }

    return output


def extract_monthly_trend_data(sales_data: pd.DataFrame, start_date: str = '2022-07-26', end_date: str = '2023-05-10') -> dict:
    """
    Extract monthly team performance metrics, ensuring all months between start_date and end_date are included.

    :param sales_data: A pandas DataFrame containing sales performance data.
    :param start_date: Start date as a string (e.g., "2023-01-01").
    :param end_date: End date as a string (e.g., "2023-12-31").
    :return: A dictionary containing monthly team performance metrics, including months with no data.
    """
    # Ensure relevant columns are numeric for calculations
    columns_to_numeric = [
        "revenue_confirmed", "avg_close_rate_30_days", "tours_booked",
        "revenue_pending", "tours_in_pipeline"
    ]
    sales_data[columns_to_numeric] = sales_data[columns_to_numeric].apply(pd.to_numeric, errors="coerce")

    # Parse the 'dated' column to datetime and create 'month_year' column
    sales_data["dated"] = pd.to_datetime(sales_data["dated"], errors="coerce")
    if sales_data["dated"].isna().all():
        raise ValueError("The dataset contains invalid or missing date information.")

    sales_data["month_year"] = sales_data["dated"].dt.strftime("%m/%Y")  # Format as MM/YYYY

    grouped = sales_data.groupby("month_year")

    all_months = pd.date_range(start=start_date, end=end_date, freq='MS').strftime("%m/%Y").tolist()

    # Initialize the result dictionary
    monthly_data = {}

    for month in all_months:
        if month in grouped.groups:  # If data exists for the month
            group = grouped.get_group(month)
            total_sales = group["revenue_confirmed"].sum()
            conversion_rate = group["avg_close_rate_30_days"].mean()
            deals_closed = group["tours_booked"].sum()
            total_tours_pipeline = group["tours_in_pipeline"].sum()
            total_revenue_pending = group["revenue_pending"].sum()
            avg_revenue_per_deal = total_sales / deals_closed if deals_closed > 0 else 0
        else:  # No data for the month
            total_sales = 0
            conversion_rate = 0
            deals_closed = 0
            total_tours_pipeline = 0
            total_revenue_pending = 0
            avg_revenue_per_deal = 0

        # Add data to the dictionary for the current month
        monthly_data[month] = {
            "total_sales": f"${total_sales}",
            "conversion_rate": f"{round(conversion_rate, 2)}%",
            "deals_closed": int(deals_closed),
            "average_revenue_per_deal": f"${round(avg_revenue_per_deal, 2)}",
            "total_tours_in_pipeline": int(total_tours_pipeline),
            "total_revenue_pending": f"${total_revenue_pending}"
        }

    # Sort the months by date
    sorted_monthly_data = OrderedDict(
        sorted(monthly_data.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y"))
    )

    return sorted_monthly_data


if __name__ == '__main__':
    filepath = os.getenv("FILE_PATH")
    sales_data = pd.read_csv(filepath)

    pprint(extract_monthly_trend_data(sales_data))
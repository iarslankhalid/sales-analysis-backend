import os
from typing import Union
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path

from app.utils.data_ingestion import extract_employee_data, extract_team_data, extract_monthly_trend_data

# Load environment variables
load_dotenv()

# Fetch API key and base URL from environment variables
XAI_API_KEY = os.getenv("XAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")

# Initialize OpenAI client
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url=BASE_URL,
)

# Create a role for the GPT model
ROLE_PROMPT = (
    """
    You are an expert Sales Performance Analyst. Your role is to analyze sales data and provide detailed feedback.
    Always return your response in the following structured format that matches an HTML template:
    
    - Section Titles: Enclosed in <h3></h3> tags.
    - Bulleted Points: Enclosed in <ul> and <li> tags.
    - Paragraphs: Use <p> tags for general descriptions.
    - Ensure all sections are clearly marked with appropriate tags.
    
    Example Format:
    <h3>Summary</h3>
    <p>The employee has shown strong performance in sales and conversions.</p>
    
    <h3>Key Strengths</h3>
    <ul>
        <li>High total sales.</li>
        <li>Excellent lead conversion rate.</li>
    </ul>
    
    <h3>Areas for Improvement</h3>
    <ul>
        <li>Focus on recurring sales.</li>
        <li>Enhance customer retention strategies.</li>
    </ul>
    
    <h3>Recommendations</h3>
    <ul>
        <li>Develop a long-term client engagement plan.</li>
        <li>Implement follow-up strategies to ensure customer satisfaction.</li>
    </ul>
    """
)



# Function to create a dynamic prompt
def create_prompt(task_type, data, period = None):
    """
    Generate a custom prompt based on the task type and input data (expected as a dictionary).
    
    :param task_type: The type of analysis (e.g., 'individual', 'team', 'trend').
    :param data: A dictionary containing relevant data for the task.
    :return: A formatted prompt string.
    """
    if task_type == "individual":
        return (
            f"Analyze the performance of Employee with the following data:\n"
            f"- Total Sales: ${data['total_sales']}\n"
            f"- Conversion Rate: {data['conversion_rate']}\n"
            f"- Deals Closed: {data['deals_closed']}\n"
            f"- Recurring Sales: ${data['recurring_sales']}\n"
            f"- Customer Retention Rate: {data['customer_retention_rate']}\n\n"
            "Provide feedback on their strengths, areas for improvement, and actionable recommendations."
        )
    
    elif task_type == "team":
        # Team-level performance analysis
        return (
            f"Give me a detailed summary about team performances"
            f"Analyze the overall performance of the sales team with the following data:\n"
            f"- Total Team Sales: ${data['total_sales']}\n"
            f"- Average Conversion Rate: {data['conversion_rate']}%\n"
            f"- Deals Closed: {data['deals_closed']}\n"
            f"- Average Revenue per Deal: {data['average_revenue_per_deal']}\n"
            f"- Total Tours in Pipeline: {data['total_tours_in_pipeline']}\n"
            f"- Total Revenue Pending: {data['total_revenue_pending']}\n"
            f"- Top Performer: {data['top_performer']}\n"
            "Provide insights into team strengths, areas for improvement, and strategies for boosting team results."
        )
    
    elif task_type == "trend":
        # Sales trend analysis
        return (
            f"analyze the given data in {period} manner, give me detailed explaination about the data, key points"
            "Identify trends, explain fluctuations, and forecast sales for the next period. Include actionable recommendations."
        )
        
    else:
        raise ValueError("Invalid task type. Choose from 'individual', 'team', or 'trend'.")


# Function to get GPT response
def get_gpt_response(prompt):
    """
    Send the prompt to the GPT model and return the generated response.
    
    :param prompt: The formatted prompt string.
    :return: The GPT model's response.
    """
    try:
        completion = client.chat.completions.create(
            model="grok-beta",  # Specify the model here
            messages=[
                {"role": "system", "content": ROLE_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        # Accessing the response correctly
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    filepath = os.getenv("FILE_PATH")  # Make sure the correct path is set in .env file
    sales_data = pd.read_csv(filepath)

    # For individual performance analysis, generate the data as a dictionary
    rep_data = extract_employee_data(sales_data, 20)  # Example: Get data for employee with ID 20
    prompt = create_prompt("individual", rep_data)
    analysis = get_gpt_response(prompt)
    print("GPT Analysis:\n", analysis)

    # Example for team analysis
    team_data = extract_team_data(sales_data)  # Get data for the entire team
    prompt = create_prompt("team", team_data)
    analysis = get_gpt_response(prompt)
    print("Team GPT Analysis:\n", analysis)
# Sales Analysis Backend

## Description
A backend system to analyze sales data using a Large Language Model (LLM) with endpoints for individual, team, and trend analysis.

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the server: `uvicorn app.main:app --reload`.

## Endpoints
1. `/api/rep_performance/`: Analyze individual performance.
2. `/api/team_performance/`: Analyze team performance.
3. `/api/performance_trends/`: Analyze sales trends.


# Project Structure
```
sales_analysis_backend/
├── app/                  
│   ├── __init__.py       
│   ├── api/              
│   │   ├── __init__.py
│   │   ├── rep_performance.py
│   │   ├── team_performance.py
│   │   ├── trends_forecast.py
│   ├── utils/            
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── gpt_integration.py
│   │   ├── feedback_generator.py
│   ├── main.py           
├── tests/                
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_utils.py
├── data/                 
│   ├── sample_sales.csv
│   ├── sample_sales.json
├── requirements.txt      
├── README.md             
├── .gitignore            
```
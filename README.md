# sales-analysis-backend
This is the assessment for Home Easy

# Project Structure
```
sales_analysis_backend/
├── app/                  # Core application code
│   ├── __init__.py       # Makes the folder a Python package
│   ├── api/              # API routes
│   │   ├── __init__.py
│   │   ├── rep_performance.py
│   │   ├── team_performance.py
│   │   ├── trends_forecast.py
│   ├── utils/            # Helper functions
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── gpt_integration.py
│   │   ├── feedback_generator.py
│   ├── main.py           # Application entry point
├── tests/                # Test cases
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_utils.py
├── data/                 # Example datasets for testing
│   ├── sample_sales.csv
│   ├── sample_sales.json
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Ignored files in Git
```
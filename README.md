# Sales Analysis Backend

## Description
A backend system to analyze sales data using a Large Language Model (LLM) with endpoints for individual, team, and trend analysis. The system provides API endpoints to analyze sales performance at different levels (individual, team, trends) by integrating LLM for deep insights.

## Technologies Used
- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.9+.
- **Uvicorn**: An ASGI server for serving FastAPI applications.
- **Pandas**: A data manipulation and analysis library.
- **Grok AI**: Used for integrating GPT-based LLM for analysis.
- **Python 3.9+**: Python version required to run this project.

## Setup

### 1. Clone the repository:
```bash
git clone https://github.com/iarslankhalid/sales-analysis-backend.git
```
### 2. Navigate to the project directory:
```bash
cd sales-analysis-backend
```
### 3. Create an API key for the Grok LLM:
Visit [Grok API Documentation](https://docs.x.ai/api) to generate your API key.

### 4. Add a `.env` file:
Create a `.env` file in the project root directory and add the following environment variables:
```bash
XAI_API_KEY="your_api_key"
BASE_URL="https://api.x.ai/v1"
FILE_PATH="your_path\\sales-analysis-backend\\data\\sales_performance_data.csv"
```

### 5. Run Setup file:
On Windows, double click or run `setup.bat`:
```bash
./setup.bat
```

On MacOS/Linux, run `setup.sh`
```bash
chmod +x ./setup.sh
./setup.sh
```

## Endpoints
1. `/api/rep_performance/`: Analyze individual sales representative performance.
2. `/api/team_performance/`: Analyze team sales performance.
3. `/api/performance_trends/`: Analyze sales trends and forecasting.

## Project Structure
```bash
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
│   │   ├── check_filepath.py
│   │   ├── data_ingestion.py
│   │   ├── gpt_integration.py
│   ├── main.py           
├── data/                 
│   ├── screenshots
│   │   ├── home.png
│   │   ├── team.png
│   │   ├── trend.png
│   ├── exercise.pdf
│   ├── sales_performance_data.csv
├── static/
│   ├── home.html
├── templates/
│   ├── rep_home.html
│   ├── rep_response.html
│   ├── team_response_light.html
│   ├── team_response.html
│   ├── trends_home.html
│   ├── trends_response.html
├── .env   
├── requirements.txt      
├── README.md             
├── .gitignore
├── setup.bat
├── setup.sh            
```

## Screenshots
Here are some screenshots for the UI:
### Home Page: [homepage](./data/screenshots/home.png)
### Team Performance Analysis: [team_performance](./data/screenshots/team.png)
### Trends Analysis: [trend_analysis](./data/screenshots/trends.png)

## Note
If you want to change the LLM API, update the `app.utils.gpt_integration` module according to the new LLM's API specifications.

#### Things to update in `gpt_integration.py`:
- Modify `BASE_URL` and `XAI_API_KEY` in your `.env` file if switching LLM services.
- Ensure the request format aligns with the new LLM's API structure.
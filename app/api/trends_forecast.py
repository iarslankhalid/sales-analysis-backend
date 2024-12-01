from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
from dotenv import load_dotenv

from app.utils.data_ingestion import extract_monthly_trend_data
from app.utils.gpt_integration import get_gpt_response, create_prompt

router = APIRouter()
templates = Jinja2Templates(directory='templates')

# Load environment variables
load_dotenv()

# Load the file path from environment variable
filepath = os.getenv("FILE_PATH")
if not filepath:
    raise ValueError("FILE_PATH environment variable is not set")

@router.get("/")
def show_trends_page(request: Request):
    """
    Renders the home page of the trends analysis.
    
    :param request: FastAPI Request object
    :return: Rendered HTML template for trends home
    """
    return templates.TemplateResponse("trends_home.html", {"request": request})


@router.get('/trend')
def analyze_trends(request: Request, period: str):
    """
    Analyzes trends for the specified period and renders the result.
    
    :param request: FastAPI Request object
    :param period: The period to analyze (e.g., 'monthly', 'quarterly')
    :return: Rendered HTML template with trends analysis results
    """
    periods = ['monthly', 'quarterly', 'half-year', 'yearly', 'overall']
    
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Trends data file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    
    if period not in periods:
        raise HTTPException(status_code=400, detail="Invalid period specified.")
    
    
    monthly_data = extract_monthly_trend_data(df)
    prompt = create_prompt('trend', monthly_data, period=period)
    response = get_gpt_response(prompt)
    response = response.replace("```html", "").replace("```", "")
    
    
    # Render the template with the trends analysis results
    return templates.TemplateResponse("trends_response.html", {
        "request": request,
        "period": period,
        "analysis": response
    })

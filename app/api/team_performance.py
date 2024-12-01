import os
import pandas as pd
from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.utils.data_ingestion import extract_team_data
from app.utils.gpt_integration import get_gpt_response, create_prompt

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Load environment variables
load_dotenv()

# Load the file path from environment variable
filepath = os.getenv("FILE_PATH")
if not filepath:
    raise ValueError("FILE_PATH environment variable is not set")

@router.get("/")
async def analyze_team_performance(request: Request):
    """
    Analyze the performance of the entire sales team.
    
    :param request: FastAPI Request object
    :return: Rendered HTML template with the team's performance analysis
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Get team data for analysis
    team_data = extract_team_data(df)
    
    if isinstance(team_data, str):
        raise HTTPException(status_code=404, detail=team_data)
    
    # Generate the prompt for GPT analysis
    prompt = create_prompt("team", team_data)
    
    # Get the response from GPT
    response = get_gpt_response(prompt)
    response = response.replace("```html", "").replace("```", "")
    
    
    # Return the rendered HTML page
    return templates.TemplateResponse("team_response.html", {
        "request": request,
        "total_sales": team_data['total_sales'],
        "conversion_rate": team_data['conversion_rate'],
        "deals_closed": team_data['deals_closed'],
        "average_revenue_per_deal": team_data['average_revenue_per_deal'],
        "total_tours_in_pipeline": team_data['total_tours_in_pipeline'],
        "total_revenue_pending": team_data['total_revenue_pending'],
        "top_performer": f"{team_data['top_performer']['employee_name']} with revenue of ${team_data['top_performer']['revenue_confirmed']}",
        "analysis": response
    })

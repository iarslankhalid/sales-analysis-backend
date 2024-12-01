import os
import pandas as pd
from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.utils.data_ingestion import extract_employee_data
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
def search_employee(request: Request):
    """
    Render the employee search page.
    
    :param request: FastAPI Request object
    :return: Rendered HTML template with the search form
    """
    return templates.TemplateResponse("rep_home.html", {"request": request})

@router.get("/performance")
def analyze_rep_performance(request: Request, rep_id: int):
    """
    Analyze the performance of a sales representative based on their ID.
    
    :param request: FastAPI Request object
    :param rep_id: ID of the sales representative
    :return: Rendered HTML template with the performance analysis
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    # Get employee data for the given rep_id
    rep_data = extract_employee_data(df, rep_id)
    
    if isinstance(rep_data, str):
        raise HTTPException(status_code=404, detail=rep_data)
    
    # Generate the prompt for GPT analysis
    prompt = create_prompt("individual", rep_data)
    
    # Get the response from GPT
    response = get_gpt_response(prompt)
    response = response.replace("```html", "").replace("```", "")
    
    return templates.TemplateResponse("rep_response.html", {
        "request": request,
        "employee_id": rep_data['employee_id'],
        "employee_name": rep_data['employee_name'],
        "analysis": response
    })

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api import rep_performance, team_performance, trends_forecast

app = FastAPI(
    title="Sales Analysis API",
    description="API to analyze sales data using LLM",
    version="1.0.0"
)

# Serve static files like images, CSS, JS if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve home page
@app.get("/", response_class=HTMLResponse)
def home():
    # Read home.html from the current directory or a specific folder
    home_path = Path(__file__).parent.parent / 'static/home.html'
    return home_path.read_text()

# Include API routes
app.include_router(rep_performance.router, prefix="/api/rep_performance", tags=["Individual Analysis"])
app.include_router(team_performance.router, prefix="/api/team_performance", tags=["Team Analysis"])
app.include_router(trends_forecast.router, prefix="/api/performance_trends", tags=["Trends and Forecasting"])



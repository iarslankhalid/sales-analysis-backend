from fastapi import APIRouter
from app.utils.gpt_integration import generate_trend_analysis

router = APIRouter()

@router.get("/")
def analyze_trends(time_period: str):
    # Mocked sales data for trends
    data = {"time_period": time_period, "sales": [120000, 150000, 180000]}
    trends = generate_trend_analysis(data)
    return {"time_period": time_period, "trend_analysis": trends}

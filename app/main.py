from fastapi import FastAPI
from app.api import rep_performance, team_performance, trends_forecast

app = FastAPI(
    title="Sales Analysis API",
    description="API to analyze sales data using LLM",
    version="1.0.0"
)

# Include API routes
app.include_router(rep_performance.router, prefix="/api/rep_performance", tags=["Individual Analysis"])
app.include_router(team_performance.router, prefix="/api/team_performance", tags=["Team Analysis"])
app.include_router(trends_forecast.router, prefix="/api/performance_trends", tags=["Trends and Forecasting"])

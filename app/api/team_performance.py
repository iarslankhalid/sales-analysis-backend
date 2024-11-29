from fastapi import APIRouter
from app.utils.feedback_generator import generate_team_feedback

router = APIRouter()

@router.get("/")
def analyze_team_performance():
    # Mocked team data
    data = [{"rep_id": 1, "sales": 120000}, {"rep_id": 2, "sales": 80000}]
    feedback = generate_team_feedback(data)
    return {"team_feedback": feedback}

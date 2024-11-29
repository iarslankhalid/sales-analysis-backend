from fastapi import APIRouter
from app.utils.feedback_generator import generate_feedback

router = APIRouter()

@router.get("/")
def analyze_rep_performance(rep_id: int):
    # Mocked data processing
    data = {"rep_id": rep_id, "sales": 120000}
    feedback = generate_feedback(data)
    return {"rep_id": rep_id, "feedback": feedback}

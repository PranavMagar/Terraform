from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_current_user(request: Request):
    return request.session.get("user_id")

@router.get("/reports")
def reports(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login")
    
    # Aggregations for initial load if needed, but we'll mostly use JS
    return templates.TemplateResponse("reports.html", {"request": request})

@router.get("/api/chart-data")
def chart_data(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user(request)
    if not user_id:
        return JSONResponse(content={"pie": {}, "line": {}})
    
    # Pie Chart: Sum by Category
    cat_data = db.query(
        models.Expense.category, func.sum(models.Expense.amount)
    ).filter(models.Expense.user_id == user_id).group_by(models.Expense.category).all()
    
    pie = {c: round(a, 2) for c, a in cat_data}

    # Line Chart: Sum by Date
    date_data = db.query(
        models.Expense.date, func.sum(models.Expense.amount)
    ).filter(models.Expense.user_id == user_id).group_by(models.Expense.date).order_by(models.Expense.date).all()
    
    line = {d.strftime("%Y-%m-%d"): round(a, 2) for d, a in date_data}

    return JSONResponse(content={"pie": pie, "line": line})

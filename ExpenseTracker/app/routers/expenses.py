from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return user_id

@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login")
    
    expenses = db.query(models.Expense).filter(models.Expense.user_id == user_id).order_by(models.Expense.date.desc()).all()
    
    total = sum(e.amount for e in expenses)
    now = datetime.now()
    month_total = sum(e.amount for e in expenses if e.date.month == now.month and e.date.year == now.year)
    avg_total = total / len(expenses) if expenses else 0
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user_expenses": expenses,
        "total": round(total, 2),
        "month_total": round(month_total, 2),
        "avg_total": round(avg_total, 2),
        "categories": ["Food", "Transport", "Bills", "Shopping", "Other"]
    })

@router.get("/add")
def add_expense_page(request: Request):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("add.html", {
        "request": request,
        "categories": ["Food", "Transport", "Bills", "Shopping", "Other"]
    })

@router.post("/add")
def add_expense(
    request: Request,
    date_str: str = Form(..., alias="date"),
    category: str = Form(...),
    amount: float = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login")
    
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return templates.TemplateResponse("add.html", {
            "request": request,
            "error": "Invalid date format",
            "categories": ["Food", "Transport", "Bills", "Shopping", "Other"]
        })

    new_expense = models.Expense(
        amount=amount,
        category=category,
        description=description,
        date=date_obj,
        user_id=user_id
    )
    db.add(new_expense)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/delete/{expense_id}")
def delete_expense(expense_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login")
    
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()
    if expense:
        db.delete(expense)
        db.commit()
    
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/edit/{expense_id}")
def edit_expense_page(expense_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login")
    
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()
    if not expense:
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "expense": expense,
        "categories": ["Food", "Transport", "Bills", "Shopping", "Other"]
    })

@router.post("/edit/{expense_id}")
def edit_expense(
    expense_id: int,
    request: Request,
    date_str: str = Form(..., alias="date"),
    category: str = Form(...),
    amount: float = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db)
):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login")
    
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()
    if not expense:
        return RedirectResponse(url="/")

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date format", 400

    expense.date = date_obj
    expense.category = category
    expense.amount = amount
    expense.description = description
    
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

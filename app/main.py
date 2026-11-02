from sqlite3 import IntegrityError

from fastapi import Depends, FastAPI, HTTPException
from opentelemetry.trace import Status
from sqlalchemy import engine
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Base, LoanDB
from app.schemas import LoanCreate, LoanRead

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loans")

@app.get("/health")
def health():
    return{"status": "ok"}

@app.post("/api/loans", response_model=LoanRead, status_code=Status.HTTP_201_CREATED)

def add_loan(new_loan: LoanCreate, db: Session = Depends(get_db())):
    db_loan = LoanDB(**new_loan.model_dump())
    db.add(db_loan)
    try:
        db.commit()
        db.refresh(db_loan)
    except IntegrityError:
        db.rolback()
        raise HTTPException(
            status_code=Status.HTTP_409_CONFlICT,
            detail="Error",
        ) 
    return db_loan

@app.get("/api/loans/{loan_id}", response_model=LoanRead)

def get_loan(loan_id: int, db: Session = Depends(get_db())):
    db_loan = db.get(LoanDB, loan_id)
    if db_loan is None:
        raise HTTPException(
            status_code=Status.HTTP_404_FOUND,
            detail = "Loan Not Found",
        )
    return db_loan


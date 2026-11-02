from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

NameStr = Annotated[str, StringConstraints(min_length = 2, max_length = 60)]
PurposeStr = Annotated[str, StringConstraints(min_length = 5, max_length = 100)]

class LoanCreate(BaseModel):
    equipment_id: int = Field(gt=0)
    borrower_name: NameStr
    loan_days: int = Field(gt=0, lt=15)
    purpose: PurposeStr

class LoadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    equipment_id: int 
    borrower_name: NameStr
    loan_days: int
    purpose: PurposeStr
    status: str

    
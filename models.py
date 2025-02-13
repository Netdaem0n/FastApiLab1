from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import date


class ResultModel(BaseModel):
    id: int | None
    competition_name : str
    place : str
    date : date
    participants : int
    ticket_price : float
    prize_pool : float
    best_result : float

    class Config:
        from_attributes = True


class ResultAll(BaseModel):
    message : str
    totall: int
    items: List[ResultModel]


class AddItem(BaseModel):
    competition_name : str
    place : str
    date : date
    participants : int
    ticket_price : float
    prize_pool : float
    best_result : float

    class Config:
        from_attributes = True

class GetByItemId(BaseModel):
    message : str
    item_id: int
    item: ResultModel | None

class TextAnswer(BaseModel):
    message: str

class MathAnswer(BaseModel):
    message: str
    value: float

class MathAnswerAll(BaseModel):
    message: str
    result: List[Dict[str, Any]]

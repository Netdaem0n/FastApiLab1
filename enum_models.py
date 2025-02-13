from enum import Enum

class SortField(str, Enum):
    id = "id"
    competition_name = "competition_name"
    place = "place"
    date = "date"
    participants = "participants"
    ticket_price = "ticket_price"
    prize_pool = "prize_pool"
    best_result = "best_result"

class SortFieldNumbers(str, Enum):
    participants = "participants"
    ticket_price = "ticket_price"
    prize_pool = "prize_pool"
    best_result = "best_result"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"
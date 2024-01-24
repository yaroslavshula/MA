import enum

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from time import time


class TicketStatus(enum.Enum):
    CREATED = 'created'
    CANCELLED = 'cancelled'
    DONE = 'done'

class Ticket(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    show_id: int
    status: TicketStatus
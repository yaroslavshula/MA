from pydantic import BaseModel, ConfigDict

from time import time

class Show(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    theater_id: int

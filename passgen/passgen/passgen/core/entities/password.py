from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Password(BaseModel):
    label: str
    owner: str
    phrase: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    password: str

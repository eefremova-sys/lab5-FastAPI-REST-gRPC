from typing import Optional
from pydantic import BaseModel

class Entry(BaseModel):
    name: str
    description: str
    reference: Optional[str] = None

class ModifyEntry(BaseModel):
    description: Optional[str] = None
    reference: Optional[str] = None
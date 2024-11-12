
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class DocumentModel(BaseModel):
    name: str
    age: Optional[int] = Field(None, description="Age of the person")
    # Add other required fields here
    additional_fields: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = 'allow'
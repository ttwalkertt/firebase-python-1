from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class DocumentModel(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier")  # New UUID field
    name: str
    age: Optional[int] = Field(None, description="Age of the person")
    creation_timestamp: datetime = Field(..., description="Timestamp of the creation")  # New field
    pets: List[str] = Field(default_factory=list, description="List of pets")  # New field
    people: List[str] = Field(default_factory=list, description="List of people")  # New field
    location: Optional[str] = Field(None, description="Location")  # New field
    summary: Optional[str] = Field(None, description="Summary")  # New field
    user_id: str = Field(..., description="User ID")  # New mandatory field
    additional_fields: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(extra='allow')
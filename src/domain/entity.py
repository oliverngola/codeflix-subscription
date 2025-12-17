from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id
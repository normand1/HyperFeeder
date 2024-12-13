from typing import List
from pydantic import BaseModel, Field


# Pydantic
class PublicationStructureComponents(BaseModel):
    """Components of a publication structure."""

    title: str = Field(description="The title of the publication")
    description: str = Field(description="The description of the publication")
    topics: List[str] = Field(description="The topics of the publication")

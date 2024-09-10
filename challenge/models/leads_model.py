# -*- coding: utf-8 -*-
"""Models module."""

from pydantic import BaseModel
from typing import List


class Lead(BaseModel):
    """Personal information."""
    name: str
    courses: List[str]

class LeadInDB(Lead):
    """"Personal information in DB."""
    id: int

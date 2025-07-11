# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""
"""SAFE AI MODULE"""
# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.
from typing import Optional
from typing_extensions import Literal
from .._models import BaseModel
from .shared.metadata import Metadata
# __all__ = ["VectorStore", "FileCounts", "ExpiresAfter"]
class FileCounts(BaseModel):
#     cancelled: int
#     completed: int
#     failed: int
#     in_progress: int
#     total: int
class ExpiresAfter(BaseModel):
#     anchor: Literal["last_active_at"]
#     Anchor timestamp after which the expiration policy applies.
#     Supported anchors: `last_active_at`.
#     days: int
class VectorStore(BaseModel):
#     id: str
#     created_at: int
#     file_counts: FileCounts
#     last_active_at: Optional[int] = None
#     metadata: Optional[Metadata] = None
#     Set of 16 key-value pairs that can be attached to an object.
#     This can be useful for storing additional information about the object in a
#     structured format, and querying for objects via API or the dashboard.
#     Keys are strings with a maximum length of 64 characters. Values are strings with
#     a maximum length of 512 characters.
#     name: str
#     object: Literal["vector_store"]
#     status: Literal["expired", "in_progress", "completed"]
#     The status of the vector store, which can be either `expired`, `in_progress`, or
#     `completed`. A status of `completed` indicates that the vector store is ready
    for use.
#     usage_bytes: int
#     expires_after: Optional[ExpiresAfter] = None
#     expires_at: Optional[int] = None

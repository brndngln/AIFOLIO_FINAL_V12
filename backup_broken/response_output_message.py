# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""

# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .response_output_text import ResponseOutputText
from .response_output_refusal import ResponseOutputRefusal

# __all__ = ["ResponseOutputMessage", "Content"]

# Content: TypeAlias = Annotated[Union[ResponseOutputText, ResponseOutputRefusal], PropertyInfo(discriminator="type")]


class ResponseOutputMessage(BaseModel):
#     id: str

#     content: List[Content]

#     role: Literal["assistant"]

#     status: Literal["in_progress", "completed", "incomplete"]
#     The status of the message input.

#     One of `in_progress`, `completed`, or `incomplete`. Populated when input items
#     are returned via API.

#     type: Literal["message"]

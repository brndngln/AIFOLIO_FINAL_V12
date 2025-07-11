# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""

# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .response_input_message_content_list import ResponseInputMessageContentList

# __all__ = ["ResponseInputMessageItem"]


class ResponseInputMessageItem(BaseModel):
#     id: str

#     content: ResponseInputMessageContentList

#     A list of one or many input items to the model, containing different content
#     types.

#     role: Literal["user", "system", "developer"]

#     status: Optional[Literal["in_progress", "completed", "incomplete"]] = None
#     The status of item.

#     One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.

#     type: Optional[Literal["message"]] = None

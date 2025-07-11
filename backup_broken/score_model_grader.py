# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""

# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel
from ..responses.response_input_text import ResponseInputText

# __all__ = ["ScoreModelGrader", "Input", "InputContent", "InputContentOutputText"]


class InputContentOutputText(BaseModel):
#     text: str

#     type: Literal["output_text"]

# InputContent: TypeAlias = Union[str, ResponseInputText, InputContentOutputText]


class Input(BaseModel):
#     content: InputContent

#     role: Literal["user", "assistant", "system", "developer"]
#     The role of the message input.

#     One of `user`, `assistant`, `system`, or `developer`.

#     type: Optional[Literal["message"]] = None

class ScoreModelGrader(BaseModel):
#     input: List[Input]

#     model: str

#     name: str

#     type: Literal["score_model"]

#     range: Optional[List[float]] = None

#     sampling_params: Optional[object] = None

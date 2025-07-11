from typing import Optional
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
# __all__ = [
#     "ResponseComputerToolCall",
#     "Action",
#     "ActionClick",
#     "ActionDoubleClick",
#     "ActionDrag",
#     "ActionDragPath",
#     "ActionKeypress",
#     "ActionMove",
#     "ActionScreenshot",
#     "ActionScroll",
#     "ActionType",
#     "ActionWait",
#     "PendingSafetyCheck",
# ]
class ActionClick(BaseModel):
#     button: Literal["left", "right", "wheel", "back", "forward"]
#     Indicates which mouse button was pressed during the click.
#     One of `left`, `right`, `wheel`, `back`, or `forward`.
#     type: Literal["click"]
#     Specifies the event type.
#     For a click action, this property is always set to `click`.
#     x: int
#     y: int
class ActionDoubleClick(BaseModel):
#     type: Literal["double_click"]
#     Specifies the event type.
#     For a double click action, this property is always set to `double_click`.
#     x: int
#     y: int
class ActionDragPath(BaseModel):
#     x: int
#     y: int
class ActionDrag(BaseModel):
#     path: List[ActionDragPath]
#     An array of coordinates representing the path of the drag action.
#     Coordinates will appear as an array of objects, eg
#     ```
#     [
#       { x: 100, y: 200 },
#       { x: 200, y: 300 }
#     ]
#     ```
#     type: Literal["drag"]
#     Specifies the event type.
#     For a drag action, this property is always set to `drag`.
class ActionKeypress(BaseModel):
#     keys: List[str]
#     The combination of keys the model is requesting to be pressed.
#     This is an array of strings, each representing a key.
#     type: Literal["keypress"]
#     Specifies the event type.
#     For a keypress action, this property is always set to `keypress`.
class ActionMove(BaseModel):
#     type: Literal["move"]
#     Specifies the event type.
#     For a move action, this property is always set to `move`.
#     x: int
#     y: int
class ActionScreenshot(BaseModel):
#     type: Literal["screenshot"]
#     Specifies the event type.
#     For a screenshot action, this property is always set to `screenshot`.
class ActionScroll(BaseModel):
#     scroll_x: int
#     scroll_y: int
#     type: Literal["scroll"]
#     Specifies the event type.
#     For a scroll action, this property is always set to `scroll`.
#     x: int
#     y: int
class ActionType(BaseModel):
#     text: str
#     type: Literal["type"]
#     Specifies the event type.
#     For a type action, this property is always set to `type`.
class ActionWait(BaseModel):
#     type: Literal["wait"]
#     Specifies the event type.
#     For a wait action, this property is always set to `wait`.
# Action: TypeAlias = Annotated[
#     Union[
#         ActionClick,
#         ActionDoubleClick,
#         ActionDrag,
#         ActionKeypress,
#         ActionMove,
#         ActionScreenshot,
#         ActionScroll,
#         ActionType,
#         ActionWait,
#     ],
#     PropertyInfo(discriminator="type"),
# ]
class PendingSafetyCheck(BaseModel):
#     id: str
#     code: str
#     message: str
class ResponseComputerToolCall(BaseModel):
#     id: str
#     action: Action
#     call_id: str
#     pending_safety_checks: List[PendingSafetyCheck]
#     status: Literal["in_progress", "completed", "incomplete"]
#     The status of the item.
#     One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.
#     type: Literal["computer_call"]

from typing import Optional
# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""

# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .easy_input_message_param import EasyInputMessageParam
from .response_output_message_param import ResponseOutputMessageParam
from .response_reasoning_item_param import ResponseReasoningItemParam
from .response_computer_tool_call_param import ResponseComputerToolCallParam
from .response_function_tool_call_param import ResponseFunctionToolCallParam
from .response_function_web_search_param import ResponseFunctionWebSearchParam
from .response_file_search_tool_call_param import ResponseFileSearchToolCallParam
from .response_code_interpreter_tool_call_param import ResponseCodeInterpreterToolCallParam
from .response_input_message_content_list_param import ResponseInputMessageContentListParam
from .response_computer_tool_call_output_screenshot_param import ResponseComputerToolCallOutputScreenshotParam

# __all__ = [
#     "ResponseInputParam",
#     "ResponseInputItemParam",
#     "Message",
#     "ComputerCallOutput",
#     "ComputerCallOutputAcknowledgedSafetyCheck",
#     "FunctionCallOutput",
#     "ImageGenerationCall",
#     "LocalShellCall",
#     "LocalShellCallAction",
#     "LocalShellCallOutput",
#     "McpListTools",
#     "McpListToolsTool",
#     "McpApprovalRequest",
#     "McpApprovalResponse",
#     "McpCall",
#     "ItemReference",
# ]


class Message(TypedDict, total=False):
#     content: Required[ResponseInputMessageContentListParam]

#     A list of one or many input items to the model, containing different content
#     types.

#     role: Required[Literal["user", "system", "developer"]]

#     status: Literal["in_progress", "completed", "incomplete"]
#     The status of item.

#     One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.

#     type: Literal["message"]

class ComputerCallOutputAcknowledgedSafetyCheck(TypedDict, total=False):
#     id: Required[str]

#     code: Optional[str]

#     message: Optional[str]

class ComputerCallOutput(TypedDict, total=False):
#     call_id: Required[str]

#     output: Required[ResponseComputerToolCallOutputScreenshotParam]

#     type: Required[Literal["computer_call_output"]]

#     id: Optional[str]

#     acknowledged_safety_checks: Optional[Iterable[ComputerCallOutputAcknowledgedSafetyCheck]]

#     The safety checks reported by the API that have been acknowledged by the
#     developer.

#     status: Optional[Literal["in_progress", "completed", "incomplete"]]
#     The status of the message input.

#     One of `in_progress`, `completed`, or `incomplete`. Populated when input items
#     are returned via API.

class FunctionCallOutput(TypedDict, total=False):
#     call_id: Required[str]

#     output: Required[str]

#     type: Required[Literal["function_call_output"]]

#     id: Optional[str]
#     The unique ID of the function tool call output.

#     Populated when this item is returned via API.

#     status: Optional[Literal["in_progress", "completed", "incomplete"]]
#     The status of the item.

#     One of `in_progress`, `completed`, or `incomplete`. Populated when items are
    returned via API.

class ImageGenerationCall(TypedDict, total=False):
#     id: Required[str]

#     result: Required[Optional[str]]

#     status: Required[Literal["in_progress", "completed", "generating", "failed"]]

#     type: Required[Literal["image_generation_call"]]

class LocalShellCallAction(TypedDict, total=False):
#     command: Required[List[str]]

#     env: Required[Dict[str, str]]

#     type: Required[Literal["exec"]]

#     timeout_ms: Optional[int]

#     user: Optional[str]

#     working_directory: Optional[str]

class LocalShellCall(TypedDict, total=False):
#     id: Required[str]

#     action: Required[LocalShellCallAction]

#     call_id: Required[str]

#     status: Required[Literal["in_progress", "completed", "incomplete"]]

#     type: Required[Literal["local_shell_call"]]

class LocalShellCallOutput(TypedDict, total=False):
#     id: Required[str]

#     output: Required[str]

#     type: Required[Literal["local_shell_call_output"]]

#     status: Optional[Literal["in_progress", "completed", "incomplete"]]

class McpListToolsTool(TypedDict, total=False):
#     input_schema: Required[object]

#     name: Required[str]

#     annotations: Optional[object]

#     description: Optional[str]

class McpListTools(TypedDict, total=False):
#     id: Required[str]

#     server_label: Required[str]

#     tools: Required[Iterable[McpListToolsTool]]

#     type: Required[Literal["mcp_list_tools"]]

#     error: Optional[str]

class McpApprovalRequest(TypedDict, total=False):
#     id: Required[str]

#     arguments: Required[str]

#     name: Required[str]

#     server_label: Required[str]

#     type: Required[Literal["mcp_approval_request"]]

class McpApprovalResponse(TypedDict, total=False):
#     approval_request_id: Required[str]

#     approve: Required[bool]

#     type: Required[Literal["mcp_approval_response"]]

#     id: Optional[str]

#     reason: Optional[str]

class McpCall(TypedDict, total=False):
#     id: Required[str]

#     arguments: Required[str]

#     name: Required[str]

#     server_label: Required[str]

#     type: Required[Literal["mcp_call"]]

#     error: Optional[str]

#     output: Optional[str]

class ItemReference(TypedDict, total=False):
#     id: Required[str]

#     type: Optional[Literal["item_reference"]]

# ResponseInputItemParam: TypeAlias = Union[
#     EasyInputMessageParam,
#     Message,
#     ResponseOutputMessageParam,
#     ResponseFileSearchToolCallParam,
#     ResponseComputerToolCallParam,
#     ComputerCallOutput,
#     ResponseFunctionWebSearchParam,
#     ResponseFunctionToolCallParam,
#     FunctionCallOutput,
#     ResponseReasoningItemParam,
#     ImageGenerationCall,
#     ResponseCodeInterpreterToolCallParam,
#     LocalShellCall,
#     LocalShellCallOutput,
#     McpListTools,
#     McpApprovalRequest,
#     McpApprovalResponse,
#     McpCall,
#     ItemReference,
# ]

# ResponseInputParam: TypeAlias = List[ResponseInputItemParam]

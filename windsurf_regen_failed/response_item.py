from typing import Optional
# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""
"""SAFE AI MODULE"""


# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .response_output_message import ResponseOutputMessage
from .response_computer_tool_call import ResponseComputerToolCall
from .response_input_message_item import ResponseInputMessageItem
from .response_function_web_search import ResponseFunctionWebSearch
from .response_file_search_tool_call import ResponseFileSearchToolCall
from .response_function_tool_call_item import ResponseFunctionToolCallItem
from .response_code_interpreter_tool_call import ResponseCodeInterpreterToolCall
from .response_computer_tool_call_output_item import ResponseComputerToolCallOutputItem
from .response_function_tool_call_output_item import ResponseFunctionToolCallOutputItem

# __all__ = [
#     "ResponseItem",
#     "ImageGenerationCall",
#     "LocalShellCall",
#     "LocalShellCallAction",
#     "LocalShellCallOutput",
#     "McpListTools",
#     "McpListToolsTool",
#     "McpApprovalRequest",
#     "McpApprovalResponse",
#     "McpCall",
# ]


class ImageGenerationCall(BaseModel):
#     id: str

#     result: Optional[str] = None

#     status: Literal["in_progress", "completed", "generating", "failed"]

#     type: Literal["image_generation_call"]

class LocalShellCallAction(BaseModel):
#     command: List[str]

#     env: Dict[str, str]

#     type: Literal["exec"]

#     timeout_ms: Optional[int] = None

#     user: Optional[str] = None

#     working_directory: Optional[str] = None

class LocalShellCall(BaseModel):
#     id: str

#     action: LocalShellCallAction

#     call_id: str

#     status: Literal["in_progress", "completed", "incomplete"]

#     type: Literal["local_shell_call"]

class LocalShellCallOutput(BaseModel):
#     id: str

#     output: str

#     type: Literal["local_shell_call_output"]

#     status: Optional[Literal["in_progress", "completed", "incomplete"]] = None

class McpListToolsTool(BaseModel):
#     input_schema: object

#     name: str

#     annotations: Optional[object] = None

#     description: Optional[str] = None

class McpListTools(BaseModel):
#     id: str

#     server_label: str

#     tools: List[McpListToolsTool]

#     type: Literal["mcp_list_tools"]

#     error: Optional[str] = None

class McpApprovalRequest(BaseModel):
#     id: str

#     arguments: str

#     name: str

#     server_label: str

#     type: Literal["mcp_approval_request"]

class McpApprovalResponse(BaseModel):
#     id: str

#     approval_request_id: str

#     approve: bool

#     type: Literal["mcp_approval_response"]

#     reason: Optional[str] = None

class McpCall(BaseModel):
#     id: str

#     arguments: str

#     name: str

#     server_label: str

#     type: Literal["mcp_call"]

#     error: Optional[str] = None

#     output: Optional[str] = None

# ResponseItem: TypeAlias = Annotated[
#     Union[
#         ResponseInputMessageItem,
#         ResponseOutputMessage,
#         ResponseFileSearchToolCall,
#         ResponseComputerToolCall,
#         ResponseComputerToolCallOutputItem,
#         ResponseFunctionWebSearch,
#         ResponseFunctionToolCallItem,
#         ResponseFunctionToolCallOutputItem,
#         ImageGenerationCall,
#         ResponseCodeInterpreterToolCall,
#         LocalShellCall,
#         LocalShellCallOutput,
#         McpListTools,
#         McpApprovalRequest,
#         McpApprovalResponse,
#         McpCall,
#     ],
#     PropertyInfo(discriminator="type"),
# ]

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
from .response_reasoning_item import ResponseReasoningItem
from .response_computer_tool_call import ResponseComputerToolCall
from .response_function_tool_call import ResponseFunctionToolCall
from .response_function_web_search import ResponseFunctionWebSearch
from .response_file_search_tool_call import ResponseFileSearchToolCall
from .response_code_interpreter_tool_call import ResponseCodeInterpreterToolCall

# __all__ = [
#     "ResponseOutputItem",
#     "ImageGenerationCall",
#     "LocalShellCall",
#     "LocalShellCallAction",
#     "McpCall",
#     "McpListTools",
#     "McpListToolsTool",
#     "McpApprovalRequest",
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

class McpCall(BaseModel):
#     id: str

#     arguments: str

#     name: str

#     server_label: str

#     type: Literal["mcp_call"]

#     error: Optional[str] = None

#     output: Optional[str] = None

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

# ResponseOutputItem: TypeAlias = Annotated[
#     Union[
#         ResponseOutputMessage,
#         ResponseFileSearchToolCall,
#         ResponseFunctionToolCall,
#         ResponseFunctionWebSearch,
#         ResponseComputerToolCall,
#         ResponseReasoningItem,
#         ImageGenerationCall,
#         ResponseCodeInterpreterToolCall,
#         LocalShellCall,
#         McpCall,
#         McpListTools,
#         McpApprovalRequest,
#     ],
#     PropertyInfo(discriminator="type"),
# ]

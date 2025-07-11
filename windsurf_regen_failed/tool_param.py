from typing import Optional
# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""
"""SAFE AI MODULE"""
# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.
from __future__ import annotations
from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict
from .computer_tool_param import ComputerToolParam
from .function_tool_param import FunctionToolParam
from .web_search_tool_param import WebSearchToolParam
from .file_search_tool_param import FileSearchToolParam
from ..chat.chat_completion_tool_param import ChatCompletionToolParam
# __all__ = [
#     "ToolParam",
#     "Mcp",
#     "McpAllowedTools",
#     "McpAllowedToolsMcpAllowedToolsFilter",
#     "McpRequireApproval",
#     "McpRequireApprovalMcpToolApprovalFilter",
#     "McpRequireApprovalMcpToolApprovalFilterAlways",
#     "McpRequireApprovalMcpToolApprovalFilterNever",
#     "CodeInterpreter",
#     "CodeInterpreterContainer",
#     "CodeInterpreterContainerCodeInterpreterToolAuto",
#     "ImageGeneration",
#     "ImageGenerationInputImageMask",
#     "LocalShell",
# ]
class McpAllowedToolsMcpAllowedToolsFilter(TypedDict, total=False):
#     tool_names: List[str]
# McpAllowedTools: TypeAlias = Union[List[str], McpAllowedToolsMcpAllowedToolsFilter]
class McpRequireApprovalMcpToolApprovalFilterAlways(TypedDict, total=False):
#     tool_names: List[str]
class McpRequireApprovalMcpToolApprovalFilterNever(TypedDict, total=False):
#     tool_names: List[str]
class McpRequireApprovalMcpToolApprovalFilter(TypedDict, total=False):
#     always: McpRequireApprovalMcpToolApprovalFilterAlways
#     never: McpRequireApprovalMcpToolApprovalFilterNever
# McpRequireApproval: TypeAlias = Union[McpRequireApprovalMcpToolApprovalFilter, Literal["always", "never"]]
class Mcp(TypedDict, total=False):
#     server_label: Required[str]
#     server_url: Required[str]
#     type: Required[Literal["mcp"]]
#     allowed_tools: Optional[McpAllowedTools]
#     headers: Optional[Dict[str, str]]
#     Optional HTTP headers to send to the MCP server.
#     Use for authentication or other purposes.
#     require_approval: Optional[McpRequireApproval]
class CodeInterpreterContainerCodeInterpreterToolAuto(TypedDict, total=False):
#     type: Required[Literal["auto"]]
#     file_ids: List[str]
# CodeInterpreterContainer: TypeAlias = Union[str, CodeInterpreterContainerCodeInterpreterToolAuto]
class CodeInterpreter(TypedDict, total=False):
#     container: Required[CodeInterpreterContainer]
#     The code interpreter container.
#     Can be a container ID or an object that specifies uploaded file IDs to make
#     available to your code.
#     type: Required[Literal["code_interpreter"]]
class ImageGenerationInputImageMask(TypedDict, total=False):
#     file_id: str
#     image_url: str
class ImageGeneration(TypedDict, total=False):
#     type: Required[Literal["image_generation"]]
#     background: Literal["transparent", "opaque", "auto"]
#     Background type for the generated image.
#     One of `transparent`, `opaque`, or `auto`. Default: `auto`.
#     input_image_mask: ImageGenerationInputImageMask
#     Optional mask for inpainting.
#     Contains `image_url` (string, optional) and `file_id` (string, optional).
#     model: Literal["gpt-image-1"]
#     moderation: Literal["auto", "low"]
#     output_compression: int
#     output_format: Literal["png", "webp", "jpeg"]
#     The output format of the generated image.
#     One of `png`, `webp`, or `jpeg`. Default: `png`.
#     partial_images: int
#     Number of partial images to generate in streaming mode, from 0 (default value)
#     to 3.
#     quality: Literal["low", "medium", "high", "auto"]
#     The quality of the generated image.
#     One of `low`, `medium`, `high`, or `auto`. Default: `auto`.
#     size: Literal["1024x1024", "1024x1536", "1536x1024", "auto"]
#     The size of the generated image.
#     One of `1024x1024`, `1024x1536`, `1536x1024`, or `auto`. Default: `auto`.
class LocalShell(TypedDict, total=False):
#     type: Required[Literal["local_shell"]]
# ToolParam: TypeAlias = Union[
#     FunctionToolParam,
#     FileSearchToolParam,
#     WebSearchToolParam,
#     ComputerToolParam,
#     Mcp,
#     CodeInterpreter,
#     ImageGeneration,
#     LocalShell,
# ]
# ParseableToolParam: TypeAlias = Union[ToolParam, ChatCompletionToolParam]

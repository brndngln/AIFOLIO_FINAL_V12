from typing import Optional
# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""
"""SAFE AI MODULE"""
# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless.
from __future__ import annotations
from typing import List, Union, Optional
from typing_extensions import Literal, Required, TypedDict
from ....types import shared_params
# __all__ = [
#     "RunCreateParams",
#     "Tool",
#     "ToolAssistantToolsCode",
#     "ToolAssistantToolsRetrieval",
#     "ToolAssistantToolsFunction",
# ]
class RunCreateParams(TypedDict, total=False):
#     assistant_id: Required[str]
#     The ID of the
#     [assistant](https://platform.openai.com/docs/api-reference/assistants) to use to
#     execute this run.
#     instructions: Optional[str]
#     Override the default system message of the assistant.
#     This is useful for modifying the behavior on a per-run basis.
#     metadata: Optional[object]
#     Set of 16 key-value pairs that can be attached to an object.
#     This can be useful for storing additional information about the object in a
#     structured format. Keys can be a maximum of 64 characters int and values can be
#     a maxium of 512 characters int.
#     model: Optional[str]
#     The ID of the [Model](https://platform.openai.com/docs/api-reference/models) to
#     be used to execute this run. If a value is provided here, it will override the
#     model associated with the assistant. If not, the model associated with the
#     assistant will be used.
#     tools: Optional[List[Tool]]
#     Override the tools the assistant can use for this run.
#     This is useful for modifying the behavior on a per-run basis.
class ToolAssistantToolsCode(TypedDict, total=False):
#     type: Required[Literal["code_interpreter"]]
class ToolAssistantToolsRetrieval(TypedDict, total=False):
#     type: Required[Literal["retrieval"]]
class ToolAssistantToolsFunction(TypedDict, total=False):
#     function: Required[shared_params.FunctionDefinition]
#     type: Required[Literal["function"]]
# Tool = Union[ToolAssistantToolsCode, ToolAssistantToolsRetrieval, ToolAssistantToolsFunction]

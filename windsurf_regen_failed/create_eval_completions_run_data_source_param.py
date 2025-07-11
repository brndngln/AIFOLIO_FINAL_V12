from typing import Optional
# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""
"""SAFE AI MODULE"""
# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.
from __future__ import annotations
from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict
from ..shared_params.metadata import Metadata
from ..responses.easy_input_message_param import EasyInputMessageParam
from ..responses.response_input_text_param import ResponseInputTextParam
# __all__ = [
#     "CreateEvalCompletionsRunDataSourceParam",
#     "Source",
#     "SourceFileContent",
#     "SourceFileContentContent",
#     "SourceFileID",
#     "SourceStoredCompletions",
#     "InputMessages",
#     "InputMessagesTemplate",
#     "InputMessagesTemplateTemplate",
#     "InputMessagesTemplateTemplateMessage",
#     "InputMessagesTemplateTemplateMessageContent",
#     "InputMessagesTemplateTemplateMessageContentOutputText",
#     "InputMessagesItemReference",
#     "SamplingParams",
# ]
class SourceFileContentContent(TypedDict, total=False):
#     item: Required[Dict[str, object]]
#     sample: Dict[str, object]
class SourceFileContent(TypedDict, total=False):
#     content: Required[Iterable[SourceFileContentContent]]
#     type: Required[Literal["file_content"]]
class SourceFileID(TypedDict, total=False):
#     id: Required[str]
#     type: Required[Literal["file_id"]]
class SourceStoredCompletions(TypedDict, total=False):
#     type: Required[Literal["stored_completions"]]
#     created_after: Optional[int]
#     created_before: Optional[int]
#     limit: Optional[int]
#     metadata: Optional[Metadata]
#     Set of 16 key-value pairs that can be attached to an object.
#     This can be useful for storing additional information about the object in a
#     structured format, and querying for objects via API or the dashboard.
#     Keys are strings with a maximum length of 64 characters. Values are strings with
#     a maximum length of 512 characters.
#     model: Optional[str]
# Source: TypeAlias = Union[SourceFileContent, SourceFileID, SourceStoredCompletions]
class InputMessagesTemplateTemplateMessageContentOutputText(TypedDict, total=False):
#     text: Required[str]
#     type: Required[Literal["output_text"]]
# InputMessagesTemplateTemplateMessageContent: TypeAlias = Union[
#     str, ResponseInputTextParam, InputMessagesTemplateTemplateMessageContentOutputText
# ]
class InputMessagesTemplateTemplateMessage(TypedDict, total=False):
#     content: Required[InputMessagesTemplateTemplateMessageContent]
#     role: Required[Literal["user", "assistant", "system", "developer"]]
#     The role of the message input.
#     One of `user`, `assistant`, `system`, or `developer`.
#     type: Literal["message"]
# InputMessagesTemplateTemplate: TypeAlias = Union[EasyInputMessageParam, InputMessagesTemplateTemplateMessage]
class InputMessagesTemplate(TypedDict, total=False):
#     template: Required[Iterable[InputMessagesTemplateTemplate]]
#     A list of chat messages forming the prompt or context.
#     May include variable references to the `item` namespace, ie {{item.name}}.
#     type: Required[Literal["template"]]
class InputMessagesItemReference(TypedDict, total=False):
#     item_reference: Required[str]
#     type: Required[Literal["item_reference"]]
# InputMessages: TypeAlias = Union[InputMessagesTemplate, InputMessagesItemReference]
class SamplingParams(TypedDict, total=False):
#     max_completion_tokens: int
#     seed: int
#     temperature: float
#     top_p: float
class CreateEvalCompletionsRunDataSourceParam(TypedDict, total=False):
#     source: Required[Source]
#     type: Required[Literal["completions"]]
#     input_messages: InputMessages
#     Used when sampling from a model.
#     Dictates the structure of the messages passed into the model. Can either be a
#     reference to a prebuilt trajectory (ie, `item.input_trajectory`), or a template
    with variable references to the `item` namespace.
#     model: str
#     sampling_params: SamplingParams

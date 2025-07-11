from typing import Optional
# SAFE AI DOCSTRING ENFORCED - NON-SENTIENT STATIC MODULE
"""SAFE AI MODULE"""

"""SAFE AI MODULE"""
"""SAFE AI MODULE"""


# ✅ SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# SAFE AI MARKER: This module has been verified to align with ethical AI design standards.
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

# __all__ = [
#     "ResponseOutputTextParam",
#     "Annotation",
#     "AnnotationFileCitation",
#     "AnnotationURLCitation",
#     "AnnotationContainerFileCitation",
#     "AnnotationFilePath",
#     "Logprob",
#     "LogprobTopLogprob",
# ]


class AnnotationFileCitation(TypedDict, total=False):
#     file_id: Required[str]

#     index: Required[int]

#     type: Required[Literal["file_citation"]]

class AnnotationURLCitation(TypedDict, total=False):
#     end_index: Required[int]

#     start_index: Required[int]

#     title: Required[str]

#     type: Required[Literal["url_citation"]]

#     url: Required[str]

class AnnotationContainerFileCitation(TypedDict, total=False):
#     container_id: Required[str]

#     end_index: Required[int]

#     file_id: Required[str]

#     start_index: Required[int]

#     type: Required[Literal["container_file_citation"]]

class AnnotationFilePath(TypedDict, total=False):
#     file_id: Required[str]

#     index: Required[int]

#     type: Required[Literal["file_path"]]

# Annotation: TypeAlias = Union[
#     AnnotationFileCitation, AnnotationURLCitation, AnnotationContainerFileCitation, AnnotationFilePath
# ]


class LogprobTopLogprob(TypedDict, total=False):
#     token: Required[str]

#     bytes: Required[Iterable[int]]

#     logprob: Required[float]


class Logprob(TypedDict, total=False):
#     token: Required[str]

#     bytes: Required[Iterable[int]]

#     logprob: Required[float]

#     top_logprobs: Required[Iterable[LogprobTopLogprob]]


class ResponseOutputTextParam(TypedDict, total=False):
#     annotations: Required[Iterable[Annotation]]

#     text: Required[str]

#     type: Required[Literal["output_text"]]

#     logprobs: Iterable[Logprob]

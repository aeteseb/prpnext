from __future__ import annotations

__all__ = ["Chat", "AsyncChat"]
from prpnext.prpnext.llm.resources.infomaniak_completions import (
    AsyncCompletions,
    AsyncCompletionsWithRawResponse,
    Completions,
    CompletionsWithRawResponse,
)
from openai._compat import cached_property
from ._resource import SyncAPIResource, AsyncAPIResource


class Chat(SyncAPIResource):
    @cached_property
    def completions(self) -> Completions:
        return Completions(self._client)

    @cached_property
    def with_raw_response(self) -> ChatWithRawResponse:
        return ChatWithRawResponse(self)


class AsyncChat(AsyncAPIResource):
    @cached_property
    def completions(self) -> AsyncCompletions:
        return AsyncCompletions(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncChatWithRawResponse:
        return AsyncChatWithRawResponse(self)


class ChatWithRawResponse:
    def __init__(self, chat: Chat) -> None:
        self._chat = chat

    @cached_property
    def completions(self) -> CompletionsWithRawResponse:
        return CompletionsWithRawResponse(self._chat.completions)


class AsyncChatWithRawResponse:
    def __init__(self, chat: AsyncChat) -> None:
        self._chat = chat

    @cached_property
    def completions(self) -> AsyncCompletionsWithRawResponse:
        return AsyncCompletionsWithRawResponse(self._chat.completions)

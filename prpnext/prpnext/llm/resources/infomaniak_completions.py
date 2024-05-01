from __future__ import annotations
from typing import Dict, Iterable, List, Literal, Mapping, Optional, Union, overload

import httpx
from openai import NOT_GIVEN, NotGiven
from openai._types import Omit
from openai.types import Completion
from openai.types.chat import ChatCompletion, ChatCompletionChunk, ChatCompletionMessageParam
from openai._streaming import Stream, AsyncStream
from openai._response import to_streamed_response_wrapper, async_to_streamed_response_wrapper
from openai._compat import cached_property
from openai._utils import required_args
from openai._base_client import make_request_options
from ._resource import SyncAPIResource, AsyncAPIResource
import openai._legacy_response as _legacy_response

Query = Mapping[str, object]
Body = object
Headers = Mapping[str, Union[str, Omit]]


class Completions(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompletionsWithRawResponse:
        return CompletionsWithRawResponse(self)
    
    @cached_property
    def with_streaming_response(self) -> CompletionsWithStreamingResponse:
        return CompletionsWithStreamingResponse(self)
    
    @overload
    def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, Literal["mixtral"]],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: Optional[Literal["standard", "creative", "strict"]] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion:
        ...

    @overload
    def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, Literal["mixtral"]],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: Optional[Literal["standard", "creative", "strict"]] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[True]] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Stream[ChatCompletionChunk]:
        ...

    @overload
    def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, Literal["mixtral"]],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: Optional[Literal["standard", "creative", "strict"]] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: bool,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        ...

    @required_args(["model", "messages"], ["messages", "model", "stream"])
    def create(
        self,
        *,
        model: Union[str, Literal["mixtral"]],
        messages: Iterable[ChatCompletionMessageParam],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: (
            Optional[Literal["standard", "creative", "strict"]] | NotGiven
        ) = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: Optional[bool] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        Creates a completion for the provided prompt and parameters.

        Args:
          model: Possible values: mixtral
          Model name to use



          messages: A list of messages to be used as context for the completion.
                Roles must alternate user/assistant/user/assistant/user/... always end with the user role

          max_new_tokens: Min: 1; Max: 5000
            Maximum number of generated tokens.

          profile_type: Possible values: standard, creative, strict
            Define parameter profiles according to your usage preferences.
            [Creativity] encourages greater diversity in text generation.
            [Standard ]settings offer a well-balanced chatbot output.
            [Strict] settings result in highly predictable generation, suitable for tasks like translation or text classification labeling.

          repetition_penalty: The repetition penalty parameter is set at 1.0, indicating no penalty.
            This parameter assists in penalizing tokens according to their frequency within the text,
            encompassing the input prompt as well.
            Tokens that have appeared five times or more receive a heavier penalty compared to tokens that have appeared just once.
            A value of 1 signifies no penalty, while values greater than 1 discourage the repetition of tokens.
            The usual range for this parameter is between 0.5 to 1.2.

          seed: A random seed to ensure reproducibility.

          stream: Stream the response. If set to true, the response will be streamed.

          system_prompt: System prompt at the beginning of the conversation with the model
            Examples:You are a helpful assistant

          temperature: Min: 0.0; Max: 1.0
            The value employed to modify the logits distribution.
            Elevated values promote greater diversity,
            whereas lower values prioritize more probable tokens.
            In typical chatbot conversations, a value of 0.6 is often used,
            while for more creative tasks, a value around 0.8 is preferred.

          top_k: Min: 1; Max: 100
            The number of highest probability vocabulary tokens to keep for top-k-filtering.
            Typical value 50 to introduces more diversity into the generated text,
            20 to produce more conservative and higher-quality samples.

          top_p: If set to < 1, only the smallest set of most probable tokens with probabilities
            that add up to top_p or higher are kept for generation.
            Typical value 0.6 for a balance between diversity and coherence.

          truncate: Min: 1; Max: 30000
            Truncate inputs tokens to the given size.

            typical_p: Min: 0.0; Max: 1.0
            Typical Decoding Mass (typical_p) refers to a parameter used in text generation algorithms,
            influencing the distribution of token probabilities during decoding.
            It signifies a typical probability value commonly employed to shape the diversity
            and coherence of generated text. Adjusting this parameter allows users to control the balance
            between these aspects, where a typical_p value guides the likelihood of certain tokens
            being selected during the generation process.
            In typical chatbot conversations, a value of 0.9 is often used.


          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        product_id = self._client.product_id
        return self._post(
            f"/{product_id}",
            body={
                "model": model,
                "messages": messages,
                "max_new_tokens": max_new_tokens,
                "profile_type": profile_type,
                "repetition_penalty": repetition_penalty,
                "seed": seed,
                "stream": stream,
                "system_prompt": system_prompt,
                "temperature": temperature,
                "top_k": top_k,
                "top_p": top_p,
                "truncate": truncate,
                "typical_p": typical_p,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ChatCompletion,
            stream=stream or False,
            stream_cls=Stream[ChatCompletionChunk],
        )


class AsyncCompletions(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompletionsWithRawResponse:
        return AsyncCompletionsWithRawResponse(self)
    
    @cached_property
    def with_streaming_response(self) -> AsyncCompletionsWithStreamingResponse:
        return AsyncCompletionsWithStreamingResponse(self)
    
    @overload
    async def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, Literal["mixtral"]],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: Optional[Literal["standard", "creative", "strict"]] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion:
        ...

    @overload
    async def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, Literal["mixtral"]],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: Optional[Literal["standard", "creative", "strict"]] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[True]] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncStream[ChatCompletionChunk]:
        ...

    @overload
    async def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, Literal["mixtral"]],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: Optional[Literal["standard", "creative", "strict"]] | NotGiven = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: bool,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        ...

    @required_args(["model", "messages"], ["messages", "model", "stream"])
    async def create(
        self,
        *,
        model: Union[str, Literal["mixtral"]],
        messages: List[Dict[str, str]],
        max_new_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        profile_type: (
            Optional[Literal["standard", "creative", "strict"]] | NotGiven
        ) = NOT_GIVEN,
        repetition_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stream: Optional[bool] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_k: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        truncate: Optional[int] | NotGiven = NOT_GIVEN,
        typical_p: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatCompletion | AsyncStream[ChatCompletionChunk]:
        """
        Creates a completion for the provided prompt and parameters.

        Args:
            model: Possible values: mixtral
            Model name to use



            messages: A list of messages to be used as context for the completion.
                Roles must alternate user/assistant/user/assistant/user/... always end with the user role

            max_new_tokens: Min: 1; Max: 5000
            Maximum number of generated tokens.

            profile_type: Possible values: standard, creative, strict
            Define parameter profiles according to your usage preferences.
            [Creativity] encourages greater diversity in text generation.
            [Standard ]settings offer a well-balanced chatbot output.
            [Strict] settings result in highly predictable generation, suitable for tasks like translation or text classification labeling.

            repetition_penalty: The repetition penalty parameter is set at 1.0, indicating no penalty.
            This parameter assists in penalizing tokens according to their frequency within the text,
            encompassing the input prompt as well.
            Tokens that have appeared five times or more receive a heavier penalty compared to tokens that have appeared just once.
            A value of 1 signifies no penalty, while values greater than 1 discourage the repetition of tokens.
            The usual range for this parameter is between 0.5 to 1.2.

            seed: A random seed to ensure reproducibility.

            stream: Stream the response. If set to true, the response will be streamed.

            system_prompt: System prompt at the beginning of the conversation with the model
            Examples:You are a helpful assistant

            temperature: Min: 0.0; Max: 1.0
            The value employed to modify the logits distribution.
            Elevated values promote greater diversity,
            whereas lower values prioritize more probable tokens.
            In typical chatbot conversations, a value of 0.6 is often used,
            while for more creative tasks, a value around 0.8 is preferred.

            top_k: Min: 1; Max: 100
            The number of highest probability vocabulary tokens to keep for top-k-filtering.
            Typical value 50 to introduces more diversity into the generated text,
            20 to produce more conservative and higher-quality samples.

            top_p: If set to < 1, only the smallest set of most probable tokens with probabilities
            that add up to top_p or higher are kept for generation.
            Typical value 0.6 for a balance between diversity and coherence.

            truncate: Min: 1; Max: 30000
            Truncate inputs tokens to the given size.

            typical_p: Min: 0.0; Max: 1.0
            Typical Decoding Mass (typical_p) refers to a parameter used in text generation algorithms,
            influencing the distribution of token probabilities during decoding.
            It signifies a typical probability value commonly employed to shape the diversity
            and coherence of generated text. Adjusting this parameter allows users to control the balance
            between these aspects, where a typical_p value guides the likelihood of certain tokens
            being selected during the generation process.
            In typical chatbot conversations, a value of 0.9 is often used.


            extra_headers: Send extra headers

            extra_query: Add additional query parameters to the request

            extra_body: Add additional JSON properties to the request

            timeout: Override the client-level default timeout for this request, in seconds
        """
        product_id = self._client.product_id
        return await self._post(
            f"/{product_id}",
            body={
                "model": model,
                "messages": messages,
                "max_new_tokens": max_new_tokens,
                "profile_type": profile_type,
                "repetition_penalty": repetition_penalty,
                "seed": seed,
                "stream": stream,
                "system_prompt": system_prompt,
                "temperature": temperature,
                "top_k": top_k,
                "top_p": top_p,
                "truncate": truncate,
                "typical_p": typical_p,
            },
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ChatCompletion,
            stream=stream or False,
            stream_cls=AsyncStream[ChatCompletionChunk],
        )


class CompletionsWithRawResponse:
    def __init__(self, completions: Completions) -> None:
        self._completions = completions

        self.create = _legacy_response.to_raw_response_wrapper(
            completions.create,
        )


class AsyncCompletionsWithRawResponse:
    def __init__(self, completions: AsyncCompletions) -> None:
        self._completions = completions

        self.create = _legacy_response.async_to_raw_response_wrapper(
            completions.create,
        )

class CompletionsWithStreamingResponse:
    def __init__(self, completions: Completions) -> None:
        self._completions = completions

        self.create = to_streamed_response_wrapper(
            completions.create,
        )


class AsyncCompletionsWithStreamingResponse:
    def __init__(self, completions: AsyncCompletions) -> None:
        self._completions = completions

        self.create = async_to_streamed_response_wrapper(
            completions.create,
        )
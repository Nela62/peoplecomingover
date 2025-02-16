import os
import json
from typing import List, Optional
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, Query, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from openai import OpenAI
from .utils.prompt import ClientMessage, convert_to_openai_messages
from .utils.tools import get_current_weather


from llama_index.llms.sambanovasystems import SambaNovaCloud
from llama_index.core.base.llms.types import (
    ChatMessage,
    MessageRole,
    ImageBlock,
    TextBlock,
)

from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
origins = [
    "http://localhost:3000",  # React app
]


# Instantiate the SambaNovaCloud model with the chosen model


load_dotenv(".env.local")

llm = SambaNovaCloud(
    model="Llama-3.2-90B-Vision-Instruct",
    context_window=100000,
    max_tokens=1024,
    temperature=0.7,
    top_k=1,
    top_p=0.01,
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


client = OpenAI(
    base_url="https://api.sambanova.ai/v1", api_key=os.environ.get("SAMBANOVA_API_KEY")
)


class Request(BaseModel):
    messages: List[dict]


# available_tools = {
#     "get_current_weather": get_current_weather,
# }


# def do_stream(messages: List[ChatCompletionMessageParam]):
#     stream = client.chat.completions.create(
#         messages=messages,
#         model="gpt-4o",
#         stream=True,
#         tools=[
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "get_current_weather",
#                     "description": "Get the current weather at a location",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "latitude": {
#                                 "type": "number",
#                                 "description": "The latitude of the location",
#                             },
#                             "longitude": {
#                                 "type": "number",
#                                 "description": "The longitude of the location",
#                             },
#                         },
#                         "required": ["latitude", "longitude"],
#                     },
#                 },
#             }
#         ],
#     )

#     return stream


# def stream_text(messages: List[ChatCompletionMessageParam], protocol: str = "data"):
#     draft_tool_calls = []
#     draft_tool_calls_index = -1

#     stream = client.chat.completions.create(
#         messages=messages,
#         model="gpt-4o",
#         stream=True,
#         tools=[
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "get_current_weather",
#                     "description": "Get the current weather at a location",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "latitude": {
#                                 "type": "number",
#                                 "description": "The latitude of the location",
#                             },
#                             "longitude": {
#                                 "type": "number",
#                                 "description": "The longitude of the location",
#                             },
#                         },
#                         "required": ["latitude", "longitude"],
#                     },
#                 },
#             }
#         ],
#     )

#     for chunk in stream:
#         for choice in chunk.choices:
#             if choice.finish_reason == "stop":
#                 continue

#             elif choice.finish_reason == "tool_calls":
#                 for tool_call in draft_tool_calls:
#                     yield '9:{{"toolCallId":"{id}","toolName":"{name}","args":{args}}}\n'.format(
#                         id=tool_call["id"],
#                         name=tool_call["name"],
#                         args=tool_call["arguments"],
#                     )

#                 for tool_call in draft_tool_calls:
#                     tool_result = available_tools[tool_call["name"]](
#                         **json.loads(tool_call["arguments"])
#                     )

#                     yield 'a:{{"toolCallId":"{id}","toolName":"{name}","args":{args},"result":{result}}}\n'.format(
#                         id=tool_call["id"],
#                         name=tool_call["name"],
#                         args=tool_call["arguments"],
#                         result=json.dumps(tool_result),
#                     )

#             elif choice.delta.tool_calls:
#                 for tool_call in choice.delta.tool_calls:
#                     id = tool_call.id
#                     name = tool_call.function.name
#                     arguments = tool_call.function.arguments

#                     if id is not None:
#                         draft_tool_calls_index += 1
#                         draft_tool_calls.append(
#                             {"id": id, "name": name, "arguments": ""}
#                         )

#                     else:
#                         draft_tool_calls[draft_tool_calls_index][
#                             "arguments"
#                         ] += arguments

#             else:
#                 yield "0:{text}\n".format(text=json.dumps(choice.delta.content))

#         if chunk.choices == []:
#             usage = chunk.usage
#             prompt_tokens = usage.prompt_tokens
#             completion_tokens = usage.completion_tokens

#             yield 'e:{{"finishReason":"{reason}","usage":{{"promptTokens":{prompt},"completionTokens":{completion}}},"isContinued":false}}\n'.format(
#                 reason="tool-calls" if len(draft_tool_calls) > 0 else "stop",
#                 prompt=prompt_tokens,
#                 completion=completion_tokens,
#             )


class ChatResponse(BaseModel):
    role: str
    content: str


@app.post("/api/chat")
async def handle_chat_data(
    req: Request,
    protocol: str = Query("data"),
):
    # messages = request.messages
    # openai_messages = convert_to_openai_messages(messages)

    # response = StreamingResponse(stream_text(openai_messages, protocol))
    # response.headers["x-vercel-ai-data-stream"] = "v1"
    # return response
    messages_data = req.messages

    # messages = []
    # for msg in messages_data:
    #     role_str = msg.get("role", "user").lower()
    #     if role_str == "system":
    #         role = MessageRole.SYSTEM
    #     elif role_str == "assistant":
    #         role = MessageRole.ASSISTANT
    #     else:
    #         role = MessageRole.USER

    #     content = msg.get("content", "")
    #     messages.append(ChatMessage(role=role, content=content))
    # # If content is a list, we assume it’s a list of blocks
    # if isinstance(content, list):
    #     blocks = []
    #     for block in content:
    #         block_type = block.get("type")
    #         if block_type == "text":
    #             blocks.append(TextBlock(text=block.get("text", "")))
    #         elif block_type == "image_url":
    #             # Assumes your client sends something like { type: "image_url", image_url: { name, url } }
    #             image_data = block.get("image_url", {})
    #             blocks.append(ImageBlock(url=image_data.get("url", "")))
    #     messages.append(ChatMessage(role=role, blocks=blocks))
    # else:
    #     messages.append(ChatMessage(role=role, content=content))

    # TODO: add structured output here to output both the assistant's response and the parameters for the tool call - store search
    # TODO: It's erroring out when I add the system message
    system_message = "The user will post a picture of their room. Rate their room as if their girlfriend or their friends is coming over and they don't want to embarrass her. Do not mention the girlfriend, just mention what the user should add / remove, include any types of furniture worth buying. You can mention any mismatched furniture that the user should get rid of and get something new instead. Give the room a rating out of 10."

    response = client.chat.completions.create(
        model="Llama-3.2-90B-Vision-Instruct",
        messages=messages_data,
    )

    print("response", response)

    # Use the SambaNova model to get a chat response
    # ai_msg = llm.chat(messages)
    # return ChatResponse(answer=ai_msg.message.content)
    return ChatResponse(role="assistant", content=response.choices[0].message.content)

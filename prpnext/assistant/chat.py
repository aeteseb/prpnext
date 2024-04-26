import json
from re import I
import frappe

from langchain_core.messages.chat import ChatMessage
from openai import chat
from prpnext.prpnext.llm.infomaniak_chat import InfomaniakChatModel
from langchain_core.output_parsers.json import JsonOutputParser

@frappe.whitelist()
def query_chat(messages: str, chat_id: str ) -> str:
    """Query the chatbot with the given messages."""
    user = frappe.session.user

    messages = json.loads(messages)
    message_list: list[ChatMessage] = [ChatMessage(content=message["message"],role= message["user"]) for message in messages]
    print(f"{chat_id=}")
    ai_chat = _get_chat(chat_id, user, message_list)
        
    chat_model = InfomaniakChatModel()
    response = chat_model.invoke(message_list)
    ai_chat.append("messages", {
        "user": user,
        "role": "user",
        "message": message_list[-1].content
    })
    ai_chat.append("messages", {
        "user": user,
        "role": "assistant",
        "message": response.content
    })
    ai_chat.save(ignore_permissions=True)
    print(response)
    return {"message": response.content, "chat_id": ai_chat.name}

def _get_chat(chat_id: str, user: str, messages: list[ChatMessage]):
    if chat_id != "null":
        chat = frappe.get_doc("AI Chat", chat_id)
        return chat
    else:
        return create_chat(user, messages)

@frappe.whitelist()
def get_chat(chat_id: str) -> dict:
    chat = frappe.get_doc("AI Chat", chat_id)
    return chat.as_dict()

def create_chat(user: str, messages: list[ChatMessage]):
    subject = _get_subject(messages[0].content)
    print(f"{subject=}")
    ai_chat = frappe.new_doc("AI Chat", user=user)
    ai_chat.subject = subject

    ai_chat.insert(ignore_permissions=True)
    return ai_chat

@frappe.whitelist()
def get_subject(chat_id: str) -> str:
    chat = frappe.get_doc("AI Chat", chat_id)
    return chat.subject

def _get_subject(message: str) -> str:
    subject_model = InfomaniakChatModel(
        system_prompt="You are a master summarizer. What is the subject of the conversation? Answer using the json format.",
    )
    jsonOutputParser = JsonOutputParser()
    subject_chain = subject_model | jsonOutputParser

    subject_response = subject_chain.invoke(message)
    print(f"{subject_response=}")
    return subject_response["subject"]

@frappe.whitelist()
def get_chat_history() -> list[dict]:
    user = frappe.session.user
    chats = frappe.get_all("AI Chat", filters={"user": user}, fields=["subject", "name"])
    print(len(chats), chats)
    return chats
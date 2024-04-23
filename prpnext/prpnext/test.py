import frappe

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

from prpnext.prpnext.llm.infomaniak_chat import InfomaniakChatModel
from dotenv import load_dotenv


@frappe.whitelist()
def test_infomaniak_chat():
    load_dotenv()
    prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
    model = InfomaniakChatModel()
    parser = StrOutputParser()
    chain = prompt | model | parser
    result = chain.invoke({"foo": "chicken"})
    print(result)
    return result

@frappe.whitelist()
def test_call():
    return "Hello World"

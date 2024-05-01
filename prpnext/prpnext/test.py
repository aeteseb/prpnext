import frappe

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

from prpnext.prpnext.llm.infomaniak_chat import InfomaniakChatModel


@frappe.whitelist()
def test_infomaniak_chat():
    api_settings = frappe.get_single("Infomaniak LLM Settings")
    print(api_settings)
    prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}")
    model = InfomaniakChatModel(
        infomaniak_api_key=api_settings.infomaniak_api_key,
        product_id=api_settings.product_id,
    )
    parser = StrOutputParser()
    chain = prompt | model | parser
    result = chain.invoke({"foo": "chicken"})
    print(result)
    return result

@frappe.whitelist()
def test_call():
    return "Hello World"

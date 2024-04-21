import frappe

@frappe.whitelist()
def test_call():
    return "Hello World"
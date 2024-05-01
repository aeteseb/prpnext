import frappe


def assert_or_raise_custom(condition: bool, exception: Exception) -> None:
    if not condition:
        raise exception


def assert_user_is_owner(doc: frappe.model.document) -> None:
    user = frappe.session.user
    assert_or_raise_custom(
        doc.owner == user,
        frappe.PermissionError(f"You are not allowed to update this {doc.doctype}"),
    )


def assert_field_value(
    doc: frappe.model.document,
    field: str,
    value: str,
    exception: Exception | None = None,
) -> None:
    if exception is None:
        exception = frappe.PermissionError(
            f"You are not allowed to update this {doc.doctype}"
        )
    assert_or_raise_custom(getattr(doc, field) == value, exception)

import json
import dateutil
import dateutil.parser
import frappe

from prpnext.assistant.utils.error_raising import assert_field_value


PREVIEW_FIELDS = [
    "name",
    "custom_title",
    "date",
    "color",
    "status",
    "priority",
    "custom_category",
]
DETAILS_FIELDS = PREVIEW_FIELDS + ["custom_assistant_description"]


def _assert_allocated_to(doc):
    user = frappe.session.user
    assert_field_value(doc, "allocated_to", user)


# ---------------------------------------------------------------------------- #
#                                      GET                                     #
# ---------------------------------------------------------------------------- #


@frappe.whitelist()
def get_todos(categories: str, status: str, priority: str) -> list:
    """Get todos based on filters"""
    filters = _get_filters(categories, status, priority)
    docs = frappe.get_all("ToDo", filters=filters, fields=PREVIEW_FIELDS)
    return [_prepare_data_for_preview(doc) for doc in docs]


@frappe.whitelist()
def get_todo_categories() -> list:
    """Get todo categories"""
    user = frappe.session.user
    return frappe.get_all("ToDo Category", user=user, fields=["title"])


@frappe.whitelist()
def get_todo_details(id: str) -> dict:
    """Get todo details"""
    doc = frappe.get_doc("ToDo", id, fields=DETAILS_FIELDS)
    _assert_allocated_to(doc)
    return _prepare_data_for_details(doc)


def _prepare_data_for_preview(doc) -> dict:
    return {
        "id": doc.name,
        "title": doc.custom_title,
        "dueDate": doc.date.isoformat() if doc.date else None,
        "color": doc.color or None,
        "status": doc.status.lower(),
        "priority": doc.priority.lower(),
        "category": doc.custom_category,
    }


def _get_description(doc) -> str | None:
    return doc.custom_assistant_description or None


def _prepare_data_for_details(doc) -> dict:
    return _prepare_data_for_preview(doc) | {"description": _get_description(doc)}


def _get_filters(
    categories: str | None, status: str | None, priority: str | None
) -> dict:
    categories: list[str] = json.loads(categories) if categories else []
    status = json.loads(status)
    priority = json.loads(priority)
    if "uncategorized" in categories:
        categories.remove("uncategorized")
        categories.append(None)
    print(["in", categories] if categories else None)
    filters = {
        "allocated_to": frappe.session.user,
        "status": status,
        "priority": priority,
    }
    if categories:
        filters["custom_category"] = ["in", categories]
    return filters


# ---------------------------------------------------------------------------- #
#                                    DELETE                                    #
# ---------------------------------------------------------------------------- #
@frappe.whitelist()
def delete_todo(id: str) -> None:
    """Delete a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.delete()


# ---------------------------------------------------------------------------- #
#                                    CREATE                                    #
# ---------------------------------------------------------------------------- #
@frappe.whitelist()
def create_todo(title: str) -> str:
    """Create a new todo and return its id"""
    user = frappe.session.user
    todo = frappe.new_doc("ToDo")
    todo.custom_title = title
    todo.allocated_to = user
    _set_description(todo, "")
    todo.save()
    # date sets automatically to current date so we need to set it to None
    todo.date = None
    todo.save()
    return todo.name


# ---------------------------------------------------------------------------- #
#                                    UPDATE                                    #
# ---------------------------------------------------------------------------- #
# ---------------------------------- Status ---------------------------------- #
@frappe.whitelist()
def close_todo(id: str) -> None:
    """Close a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.status = "Closed"
    doc.save()


@frappe.whitelist()
def cancel_todo(id: str) -> None:
    """Cancel a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.status = "Cancelled"
    doc.save()


@frappe.whitelist()
def reopen_todo(id: str) -> None:
    """Reopen a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.status = "Open"
    doc.save()


# --------------------------------- CATEGORY --------------------------------- #
@frappe.whitelist()
def set_category(id: str, category: str) -> None:
    """Set category for a todo"""
    category_doc = (
        _get_category_doc(category)
        if category not in ["uncategorized", "null"]
        else None
    )
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.custom_category = category_doc
    doc.save()


def _get_category_doc(category: str) -> frappe.model.document:
    user = frappe.session.user
    try:
        doc = frappe.get_doc("ToDo Category", category, user=user)
        _assert_allocated_to(doc)
        return doc
    except frappe.DoesNotExistError:
        doc = frappe.new_doc("ToDo Category", user=user, title=category)
        doc.save()
        return doc


# --------------------------------- PRIORITY --------------------------------- #
@frappe.whitelist()
def set_priority(id: str, priority: str) -> None:
    """Set priority for a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.priority = priority.capitalize()
    doc.save()


# ----------------------------------- COLOR ---------------------------------- #
@frappe.whitelist()
def set_color(id: str, color: str) -> None:
    """Set color for a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.color = color if color != "null" else None
    doc.save()


# ----------------------------------- DATE ----------------------------------- #
@frappe.whitelist()
def set_due_date(id: str, date: str) -> None:
    """Set date for a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.date = dateutil.parser.parse(date.strip('"')) if date != "null" else None
    doc.save()


# --------------------------------- DESCRIPTION ------------------------------- #
@frappe.whitelist()
def set_description(id: str, description: str) -> None:
    """Set description for a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    _set_description(doc, description)


def _set_description(doc, description: str | None):
    doc.custom_assistant_description = description
    doc.description = doc.custom_title


# ----------------------------------- TITLE ---------------------------------- #
@frappe.whitelist()
def set_title(id: str, title: str) -> None:
    """Set title for a todo"""
    doc = frappe.get_doc("ToDo", id)
    _assert_allocated_to(doc)
    doc.custom_title = title
    doc.save()

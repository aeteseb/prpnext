import frappe

@frappe.whitelist()
def get_assistant_settings():
    user = frappe.session.user
    try:
        app_settings = frappe.get_doc("Assistant App Settings", user)
    except frappe.DoesNotExistError as e:
        print(e)
        print("Creating new settings")
        app_settings = frappe.new_doc("Assistant App Settings")
        app_settings.check_permission(permtype='write')
        app_settings.user = user
        app_settings.theme_mode = "dark"
        app_settings.seed_color = "FF8BC34A"
        app_settings.insert(ignore_permissions=True)
        frappe.db.commit()
    
    return {
        "themeMode": app_settings.theme_mode,
        "seedColor": app_settings.seed_color
    }

@frappe.whitelist()
def set_theme_mode(theme_mode):
    user = frappe.session.user
    app_settings = frappe.get_doc("Assistant App Settings", user)
    app_settings.theme_mode = theme_mode
    app_settings.save(ignore_permissions=True)
    

@frappe.whitelist()
def set_seed_color(seed_color):
    user = frappe.session.user
    app_settings = frappe.get_doc("Assistant App Settings", user)
    app_settings.seed_color = seed_color
    app_settings.save(ignore_permissions=True)
    
    return app_settings.seed_color
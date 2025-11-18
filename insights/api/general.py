import frappe
from frappe.translate import get_all_translations


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_translations():
    """Insights için aktif dile göre çeviri sözlüğünü döndür.

    Helpdesk'teki get_translations ile aynı davranışı izler; böylece
    frontend tarafında frappe-ui resource ile tek seferde tüm msgid→msgstr
    eşleşmeleri alınabilir.
    """
    language = None
    if frappe.session.user != "Guest":
        language = frappe.db.get_value("User", frappe.session.user, "language")
    if not language:
        language = frappe.db.get_single_value("System Settings", "language")
    return get_all_translations(language)


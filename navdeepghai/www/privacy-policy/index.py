'''
'''
import frappe

no_cache = True

def get_context(context):
    boot_context = context.get("boot_context")
    if(boot_context.get("privacy_policy")
        and frappe.db.get_value("Company Privacy Policy", boot_context.get("privacy_policy"))):
        context.update({
            "privacy_policy": frappe.get_doc("Company Privacy Policy", boot_context.get("privacy_policy"))
        })

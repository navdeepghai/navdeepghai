'''
'''
import frappe

no_cache = True

def get_context(context):
    boot_context = context.get("boot_context")
    if(boot_context.get("terms_and_conditions")
        and frappe.db.get_value("Company Terms and Conditions", boot_context.get("terms_and_conditions"))):
        context.update({
            "terms_and_conditions": frappe.get_doc("Company Terms and Conditions", boot_context.get("terms_and_conditions"))
        })

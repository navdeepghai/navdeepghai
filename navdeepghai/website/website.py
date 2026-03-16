'''
    Controller to control the context for every
    Single page
'''
import frappe
from frappe import _
import json

def update_website_context(context):
    # Update all the default context values
    try:
        update_meta_tags(context)
        system_defaults = get_default_settings()
        update_boot_context(context)
    except Exception:
        frappe.logger().error("Failed to update website context", exc_info=True)


def update_meta_tags(context):
    items = {}
    for web_meta in frappe.db.sql("""SELECT name FROM `tabWebsite Route Meta`  WHERE name = '/index' """, as_dict=True):
        metatag = frappe.get_doc("Website Route Meta", web_meta.name)
        for tag in metatag.meta_tags:
            tag.set_in_context(context)
    return items

SETTINGS = ['timing_availability', 'announcement', 'latitude', 'longitude',
    'disable_calendar', 'disabled_message', 'terms_and_conditions',
    'privacy_policy', "mobile_no", "it_email"
]
def update_boot_context(context):
    global SETTINGS
    settings = frappe.get_doc("Websites Settings", "Websites Settings")
    boot_context = {}
    for key in SETTINGS:
        boot_context[key] = settings.get(key) or ""
    context.update({
        "boot_context": boot_context,
        "settings": settings.as_dict()
    })

SYS_DEFAULTS = ['default_country', 'time_zone', 'lang',
'date_format']
@frappe.whitelist(allow_guest=True)
def get_default_settings():
    global SYS_DEFAULTS
    settings = frappe.get_doc("System Settings", "System Settings").as_dict()
    values = frappe._dict()
    for key, val in settings.items():
        if key in SYS_DEFAULTS:
            values[key] = val
    return values

'''
'''

import frappe
from frappe import _

no_cache=True

def get_context(context):
    context.update({
        "resume": frappe.get_doc("Website Resume", "navdeepghai1@gmail.com").as_dict()
    })

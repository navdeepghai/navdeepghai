'''
'''

import frappe
from frappe import _

def get_data():
    return [{
        "label": "Setup Dashboard",
        "items":[{
			"type": "doctype",
			"name": "G Dashboard",
			"description": _("Make Dashboard Sidebar, Dashboard"),
		}]
    }]

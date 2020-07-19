'''
'''

import frappe
from frappe import _

def get_data():
    return [{
            "label": "Geo Data",
            "items":[{
    			"type": "doctype",
    			"name": "Germbusters Settings",
    			"description": _("Germbusters Settings"),
            },{
    			"type": "doctype",
    			"name": "Company Settings",
    			"description": _("Company Settings for each Region"),
    		},{
    			"type": "doctype",
    			"name": "Service Technician",
    			"description": _("Service Technician"),
            },{
    			"type": "doctype",
    			"name": "Disinfection System",
    			"description": _("Disinfection System"),
            }]
    }]

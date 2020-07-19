'''
'''
import frappe
from frappe import _

def get_data():
    return [{
        "label": _("Website Settings"),
        "items":[{
            "type": "doctype",
            "name": "About Us",
            "description": _("Website Page About Us"),
        },{
            "type": "doctype",
            "name": "Custom Website Settings",
            "description": _("Custom Website Settings"),
        },{
            "type": "doctype",
            "name": "Company Privacy Policy Item",
            "description": _("Company Privacy Policy"),
        },{
            "type": "doctype",
            "name": "Company Terms and Conditions",
            "description": _("Company Terms and Conditions"),
        },{
            "type": "doctype",
            "name": "Website Image Set",
            "description": _("Set Images for website and route"),
        },{
            "type": "doctype",
            "name": "Website Image",
            "description": _("Website Image"),
        },{
            "type": "doctype",
            "name": "Website Card",
            "description": _("Website Card"),
        },{
            "type": "doctype",
            "name": "Website Carousel",
            "description": _("Website Carousel"),
        }]
    }]


'''
'''
import frappe
from germbusters.tracking.utils.geocoding_utils import get_address_information

no_cache=True

def get_context(context):
    doc = frappe.get_doc("About Us", "About Us")
    context.update({
        "aboutus": doc
    })


@frappe.whitelist(allow_guest=True)
def get_company_location():
    aboutus = frappe.get_doc("About Us", "About Us")
    template = "germbusters/templates/includes/aboutus/address_template.html"
    long_address = "820 US-1 Iselin, NJ 08830 US"
    default_company_address = {
        "title": "Office Location",
        "street_name": "820 US-1",
        "city": "Iselin",
        "state": "NJ",
        "zip_code": "08830"
    }
    if (aboutus.company_address and frappe.db.get_value("Address", aboutus.company_address)):
        address = frappe.get_doc("Address", aboutus.company_address)
        default_company_address.update({
            "title": address.address_title,
            "street_name": address.address_line1,
            "city": address.city,
            "state": address.state,
            "zip_code": address.pincode
        })
        long_address = "%s %s, %s %s %s"%(address.address_line1, address.city,
            address.state, address.pincode, address.country)

    location = frappe.render_template(template, default_company_address)
    return {
        "location":location,
        "long_address": long_address
    }

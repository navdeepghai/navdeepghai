'''
'''

import frappe
from frappe.utils import cstr
import json
from six import string_types
from frappe import _

@frappe.whitelist(allow_guest=True)
def save_doc(doctype, doc, args):
    if(doc and isinstance(doc, string_types)):
        doc = frappe._dict(json.loads(doc))

    if(args and isinstance(args, string_types)):
        args = frappe._dict(json.loads(args))

    doc.update({
        "doctype": doctype,
        "docstatus": 1
    })
    frappe.set_user("support@mygermbusters.com")

    if(args):
        for key, val in args.items():
            doc[key] = val
    try:
        doc = frappe.get_doc(doc)
        doc.save(ignore_permissions=True);
        return doc.as_dict()
    except Exception as e:
        print(frappe.get_traceback())
        raise e

@frappe.whitelist(allow_guest=True)
def get_fields(doctype):
    data = frappe._dict()
    doc = None
    if(frappe.db.exists("DocType", doctype)):
        doc = frappe.get_doc("DocType", doctype)
    if(doc):
        for field in doc.fields:
            if(field.fieldtype == "Table"):
                continue
            data.setdefault("fields", [])
            if(field.fieldtype == "Link"):
                field.fieldtype = "Select"
                options = [f.name for f in frappe.db.sql("""SELECT name FROM `tab%s` ORDER BY NAME"""%(field.options), as_dict=True)]
                field.options = "\n".join(options)

            data.fields.append(field.as_dict())
    return data

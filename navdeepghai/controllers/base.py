'''
    Develoer Navdeep
    Email navdeep@blox.ae
'''

import frappe
from frappe import _, msgprint, throw
import json
from frappe.utils import flt

class BaseController(object):
    def __init__(self, doc, doctype, method):
        self.doc = doc
        self.doctype  = doctype
        self.method = method
        self.setting = None
        self.company_setting = None

    def validate(self):
        print("Base Controller")
        print("Doctype = {0}".format(self.doctype))
        self.update_default_settings()

    def on_cancel(self):
        print("Base Controller")
        print("Doctype = {0}".format(self.doctype))
        self.update_default_settings()

    def on_submit(self):
        print("Base Controller")
        print("Doctype = {0}".format(self.doctype))
        self.update_default_settings()

    def update_default_settings(self):
        pass

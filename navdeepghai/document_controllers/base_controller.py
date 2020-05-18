'''
	Developer Navdeep
	Email navdeepghai1@gmail.com
'''

import frappe
from frappe import _, msgprint, throw, scrub
import os, importlib

APP_NAME  = "navdeepghai"
BASE_FOLDER = "document_controllers"

ALLOWED_DOCTYPES = [
	'Task', 'Payment Entry', 'Sales Invoice'
	]

'''
	Base handler for all the document controller
'''
def handler(doc, method=None):

	DOCTYPE = doc.meta.name
	if DOCTYPE not in ALLOWED_DOCTYPES:
		return
	try:
		_class = None
		path = "%s.%s.%s"%(APP_NAME, BASE_FOLDER, scrub(DOCTYPE))
		_module = importlib.import_module(path)
		_class  = getattr(_module, DOCTYPE.replace(" ", "").replace("-", ""), None)
		if _class:
			_func = getattr(_class(doc, DOCTYPE, method), method, None)
			if _func:
				_func()

	except  ImportError as e:
		print(frappe.get_traceback())
		raise e

'''
Before naming series for all the doctype
'''
def before_naming_series(doc, method):
	if hasattr(doc, "company") and getattr(doc, "company", None):
		doc.abbr = frappe.db.get_value("Company", doc.company, "abbr")

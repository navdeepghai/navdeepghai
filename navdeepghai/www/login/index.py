'''
'''
from frappe.www.login import *
from frappe.www.login import get_context as login_context

no_cache = True
def get_context(context):
	login_context(context)

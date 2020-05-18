# -*- coding: utf-8 -*-
# Copyright (c) 2020, GERMBUSTERS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _, get_module_path
import os
import importlib
from frappe.utils import getdate, nowdate, now_datetime, nowtime

MODULE_NAME  = 'dashboard'
APP_NAME = "germbusters"
IGNORE_FIELDTYPES = ['Section Break', 'Column Break']

class GDashboard(Document):

	def validate(self):
		self.update_defaults()
		self.validate_role_profile()
		self.update_standard_filters()
		self.validate_sidebar_items()
		self.update_columns_details()
		self.make_js_controller()

	def update_defaults(self):
		self._doc = frappe.get_doc("DocType", self.name)
		self._custom_fields = frappe.db.sql("""SELECT *  FROM `tabCustom Field`
			WHERE dt='%s'"""%(self._doc.name), as_dict=True)
		self._fields = self._doc.fields + self._custom_fields

	def validate_role_profile(self):
		if(not self.is_default and self.default_items):
			self.set("default_items", [])

		roles = ", ".join(["'%s'"%(r.role_profile) for r in self.default_items])
		if(roles):
			existing_roles = "<br>".join(["<b>%s: </b>:%s "%(r.parent, r.role_profile) for r in \
									frappe.db.sql("""SELECT role_profile, parent FROM `tabG Dashboard Role Profile`
										WHERE role_profile in (%s) AND parent != '%s' """%(roles, self.name), as_dict=True)])
			if(existing_roles):
				frappe.throw(_("Default dashboard already exists for following roles:<br><br>%s"%(existing_roles)))

	def update_standard_filters(self):
		if(self.filters):
			return
		for field in self._fields:
			if not field.in_standard_filter:
				continue

			flag = False
			for filter in self.filters:
				if(field.fieldname == filter.fieldname):
					if not filter.label:
						# Set default label
						filter.label = field.label
					# Update fieldname and label
					filter.fieldname = field.fieldname
					filter.fieldtype = field.fieldtype
					flag = True
					break
			if not flag:
				self.append("filters", {
					"label": field.label,
					"fieldtype": field.fieldtype,
					"fieldname": field.fieldname,
					"options": field.options,
					"read_only": field.read_only,
					"columns": field.columns,
				})

	def validate_sidebar_items(self):
		for s in self.sidebar_items:
			if s.sidebar_doctype == self.name:
				frappe.throw(_("You can't link to same sidebar dashboard (%s) at row #%s"%(s.sidebar_doctype, s.idx)))

	def make_js_controller(self):
		global MODULE_NAME
		module_path = get_module_path(MODULE_NAME, "g_dashboard", self.name)
		name = frappe.scrub(self.name)
		js_controller_path = os.path.join(module_path, "%s.js"%(name))
		py_controller_path = os.path.join(module_path, "%s.py"%(name))
		page_controller_path = os.path.join(module_path, "page_%s.js"%(name))

		module_controller_path = os.path.join(module_path, "__init__.py")

		if(not os.path.exists(module_path)):
			try:
				os.mkdir(module_path)
			except OSError as e:
				frappe.throw(e)
		# JS controller
		if(not os.path.exists(js_controller_path)):
			with open(js_controller_path, "w") as f:
				f.write("/* write your js controller here */")

		# Python Controller
		if(not os.path.exists(py_controller_path)):
			with open(py_controller_path, "w") as f:
				f.write("""\"\"\"\n	Write your python controller here\n\"\"\"\n
					\nimport frappe\n\ndef execute(filters={}, dashboard=None):\n	pass
				 """)
		if(not os.path.exists(module_controller_path)):
			with open(module_controller_path, "w") as f:
				pass

		if(self.enable_page and not os.path.exists(page_controller_path)):
			with open(page_controller_path, "w") as f:
				f.write("/* write your page js controller here */")

		self.js_controller_path  = "germbusters/dashboard/g_dashboard/{name}/{name}.js".format(name=name)
		self.page_js_controller_path = "germbusters/dashboard/g_dashboard/{name}/page_{name}.js".format(name=name)

	def update_columns_details(self):
		global IGNORE_FIELDTYPES
		if(self.columns_details):
			return
		for field in self._fields:
			if field.fieldtype in IGNORE_FIELDTYPES:
				continue
			self.append("columns_details", {
				"fieldname": field.fieldname,
				"label": field.label or field.fieldname.title()
			})

# Get dashboard module path
def get_dashboard_module_path(dashboard):
	global MODULE_NAME
	module_path = get_module_path(MODULE_NAME, "g_dashboard", dashboard)
	return module_path

# Get full path
def get_js_controller_path(dashboard):
	dashboard = frappe.scrub(dashboard)
	return os.path.join(get_dashboard_module_path(dashboard), "%s.js"%(dashboard))

# Get Py controller path
def execute_controller(dashboard, filters):
	global MODULE_NAME, APP_NAME
	dashboard_name = frappe.scrub(dashboard.name)
	try:
		_class = None
		path = "%s.%s.%s.%s.%s"%(APP_NAME, MODULE_NAME, "g_dashboard", dashboard_name, dashboard_name)
		_module = importlib.import_module(path)
		_func = getattr(_module, "execute", None)
		if _func:
			return _func(filters, dashboard)
	except  ImportError as e:
		print(frappe.get_traceback())
		raise e

def update_dashboard_filters(dashboard):
	for f in dashboard.get("filters") or []:
		if(f.fieldtype == "Date" and f.is_default):
			f.default = nowdate()
		if(f.fieldtype == "Datetime" and f.is_default):
			f.default = now_datetime()
		if(f.fieldtype == "Time" and f.is_default):
			f.default = nowtime()

def get_default_dashboard_role_profile():
	user_dict = frappe._dict()
	for r in frappe.db.sql("""SELECT `tabG Dashboard Role Profile`.role_profile, `tabUser`.name as user,
				`tabG Dashboard Role Profile`.parent AS dashboard
				FROM `tabG Dashboard Role Profile` INNER JOIN `tabUser`
				ON `tabG Dashboard Role Profile`.role_profile = `tabUser`.role_profile_name""", as_dict=True):
		user_dict.setdefault(r.user, []);
		user_dict[r.user].append(r.dashboard)
	return user_dict

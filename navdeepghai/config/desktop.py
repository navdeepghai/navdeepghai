# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [{
			"module_name": "NavdeepGhai",
			"color": "grey",
			"icon": "octicon octicon-settings",
			"type": "module",
			"label": _("Navdeep Ghai")
		},{
			"module_name": "Dashboard",
			"color": "grey",
			"icon": "octicon octicon-dashboard",
			"type": "module",
			"label": _("Dashboard")
		},{
			"module_name": "Custom Website",
			"color": "grey",
			"icon": "fa fa-safari",
			"type": "module",
			"label": _("Custom Website")
		}]

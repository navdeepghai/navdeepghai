# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Germbusters",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("Germbusters")
		},{
			"module_name": "Tracking",
			"icon": "fas fa-search-location",
			"type": "module",
			"label": _("Tracking")
		},{
			"module_name": "Germbusters",
			"type": "module",
			"label": _("Germbusters")
		}
	]

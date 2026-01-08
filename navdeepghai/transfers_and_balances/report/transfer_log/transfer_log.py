# Copyright (c) 2025, NavdeepGhai and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import fmt_money, flt


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"fieldtype": "Date",
			"fieldname": "transfer_date",
			"labe": _("Transfer Date")
		},{
			"label": _("Transfer By"),
			"fieldname": "transfer_by",
			"fieldtype": "Data"
		},{
			"label": _("Transfer To"),
			"fieldname": "transfer_to",
			"fieldtype": "Data"
		},{
			"label": _("Total Transfer"),
			"fieldname": "total_transfer",
			"fieldtype": "Data"
		},{
			"label": _("Transfer Method"),
			"fieldname": "transfer_method",
			"fieldtype": "Data"
		}
	]


def get_data() -> list[frappe._dict]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	results = []
	for item in frappe.get_all("Transfer Log", fields="*"):
		item.total = item.total_transfer
		item.total_transfer = fmt_money(item.total_transfer, currency="INR")
		results.append(item)

	total_row = sum([flt(t.total) for t in results])
	results.append({
		"transfer_to": "Total",
		"total_transfer": fmt_money(total_row, currency="INR"),
	})

	return results

"""
	Write your python controller here
"""

import frappe

def execute(filters={}, dashboard=None):
	conditions = get_conditions(filters, dashboard)

	data = []
	for res in frappe.db.sql(""" SELECT `tabVehicle`.name, `tabVehicle`.employee
	 		FROM
				`tabVehicle` INNER JOIN `tabVehicle Log`
			WHERE `tabVehicle`.docstatus = 0 %s"""%(conditions), as_dict=True):
		data.append({
			"status": "Test",
			"vehicle_details": res.name
		})
	return data


def get_conditions(filters, dashboard):
	conditions = ""
	assigned_vehicles = ", ".join(["'%s'"%(v.for_value) for v in frappe.db.sql(""" SELECT for_value FROM `tabUser Permission`
			WHERE allow='Vehicle' AND user='%s'
		"""%(frappe.session.user), as_dict=True)])

	if(assigned_vehicles):
		conditions += " AND `tabVehicle`.name IN (%s) "%(assigned_vehicles)

	return conditions

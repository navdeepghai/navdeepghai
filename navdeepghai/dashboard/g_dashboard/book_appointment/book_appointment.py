"""
	Write your python controller here
"""


import frappe
from germbusters.boot import get_default_datetime_format
from germbusters.booking.doctype.book_appointment.book_appointment import pretty_format_minutes
from frappe.utils import getdate, nowdate, get_datetime
from frappe import string_types
import json

def execute(filters={}, dashboard=None):
	return get_booking_list(filters)

def get_booking_list(filters):
	user = frappe.session.user
	booking_date = getdate(filters.get("booking_date"));

	default_format = get_default_datetime_format()
	conditions = get_employee_conditions(user)
	data = []
	results = frappe.db.sql("""SELECT `tabBook Appointment`.name,
	        `tabBook Appointment`.full_name, `tabBook Appointment`.mobile,
	        `tabBook Appointment`.email, `tabBook Appointment`.customer_address,
	        `tabBook Appointment`.to_time_data, `tabBook Appointment`.booking_date,
	        `tabBook Appointment`.customer_address_without_country,
	        `tabBook Appointment`.appointment_start_time,
	        `tabBook Appointment`.from_time, `tabBook Appointment`.to_time,
	        `tabBook Appointment`.target_details, `tabBook Appointment`.disinfection_system,
	        `tabBook Appointment`.total_targets,
	        `tabBook Appointment`.status, `tabBook Appointment Employee`.task
	        FROM `tabBook Appointment` INNER JOIN `tabBook Appointment Employee`
	        ON `tabBook Appointment`.name = `tabBook Appointment Employee`.parent
	        WHERE
	            `tabBook Appointment`.docstatus != 2 AND
	            `tabBook Appointment`.booking_date >= '%s' %s
	        ORDER BY
	            `tabBook Appointment`.appointment_start_time
	        """%(booking_date, conditions), as_dict=True)

	for res in results:
	    time_diff  = ""
	    if(res.appointment_start_time):
	        time_diff = pretty_format_minutes((res.to_time-res.appointment_start_time).seconds)
	    res.update({
	        "booking_date": res.booking_date.strftime(default_format.date_format),
	        "from_time": res.from_time.strftime(default_format.time_format),
	        "appointment_start_time": res.appointment_start_time.strftime(default_format.time_format) if res.appointment_start_time else "",
	        "etc": time_diff
	    })
	    data.append(res)
	return data

# GET SERVICE TECHNICIAN
def get_employee_conditions(user):
	employees = ", ".join(["'%s'"%(e.for_value) for e in frappe.db.sql("""
		SELECT for_value FROM `tabUser Permission` WHERE allow='Employee'
		AND user='%s' """%(user), as_dict=True)])
	conditions = " AND `tabBook Appointment Employee`.employee IN (%s) "%(employees or 'NULL')
	return conditions

@frappe.whitelist()
def get_booking_detail(booking):
    data = {}
    if(booking and frappe.db.exists("Book Appointment", booking)):
        data = frappe.get_doc("Book Appointment", booking).as_dict()
    return data

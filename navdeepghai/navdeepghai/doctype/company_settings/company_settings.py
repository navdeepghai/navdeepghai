# -*- coding: utf-8 -*-
# Copyright (c) 2020, GERMBUSTERS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class CompanySettings(Document):

	def validate(self):
		self.update_service_details()

	def update_service_details(self):
		self.update_commercial_items()
		self.update_vehicle_items()
		self.update_residentail_items()

	def update_commercial_items(self):
		for item in self.service_items:
			self.validate_and_get_item_price(item)

	def update_vehicle_items(self):
		for item in self.vehicle_items:
			self.validate_and_get_item_price(item)

	def update_residentail_items(self):
		for item in self.residential_items:
			self.validate_and_get_item_price(item)

	def validate_and_get_item_price(self, item):
		price_list = frappe.db.get_value("Price List", {"disinfection_system": item.disinfection_system})
		if(not price_list):
			frappe.throw(_("Setup price list for item %s at row #%s for %s"%(item.item, item.idx,
																		item.disinfection_system)))
		price_list_rate = frappe.db.get_value("Item Price", {"item_code": item.item, "price_list": price_list},
					"price_list_rate")

		if(price_list and not price_list_rate):
			frappe.throw(_("Setup item price for item %s at row #%s for %s"%(item.item, item.idx, item.disinfection_system)))

		temp = frappe.get_doc("Item", item.item)	
		item.update({
			"price": price_list_rate,
			"item_group": temp.item_group,
			"price_list": price_list
		})

# -*- coding: utf-8 -*-
# Copyright (c) 2020, NavdeepGhai and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint, cstr

class WebsiteResume(Document):

	def validate(self):
		self.validate_full_name()

	def validate_full_name(self):
		self.full_name = cstr("%s %s"%(self.first_name, self.last_name)).title()

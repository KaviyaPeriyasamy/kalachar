# -*- coding: utf-8 -*-
# Copyright (c) 2020, av2l and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UserInformation(Document):
	pass
@frappe.whitelist()
def authenticate_user(phone_no,password):
	s=[]
	User_information_doc=frappe.get_doc("User Information",phone_no)
	if password==User_information_doc.password:
		s.append("allowed")
	else:
		s.append("not allowed")
	return s

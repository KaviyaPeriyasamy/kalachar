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
@frappe.whitelist()
def get_dancer_detail(type_,purpose):
	category={}
	dancers=[]
	dancer_list=frappe.get_all("User Information",filters={'dance_type':type_,'purpose':purpose})
	for dancer in dancer_list:
		dancer_doc=frappe.get_doc("User Information",dancer.name)
		category['org_name']=dancer_doc.organization_name
		category['org_addr']=dancer_doc.organization_address
		category['org_phone']=dancer_doc.organization_phone_number
		for charges in dancer_doc.charging_details:
			if charges.purpose==purpose and charges.dance_type==type_:
				category['timing']=charges.timing
				category['advance_amount']=charges.advance_amount
				category['full_amount']=charges.full_amount
		dancers.append(category)
	print(dancers)
	return dancers



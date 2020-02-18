# -*- coding: utf-8 -*-
# Copyright (c) 2020, av2l and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UserInformation(Document):
	pass
@frappe.whitelist(allow_guest=True)
def authenticate_user(phone_no,password):
	s=[]
	User_information_doc=frappe.get_doc("User Information",phone_no)
	if password==User_information_doc.password:
		s.append("allowed")
	else:
		s.append("not allowed")
	return s
@frappe.whitelist(allow_guest=True)
def get_dancer_detail(type_,purpose):
	dancers=[]
	dancer_list=frappe.get_all("User Information",filters={'dance_type':type_,'purpose':purpose})
	for dancer in dancer_list:
		category={}
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
	return dancers
@frappe.whitelist(allow_guest=True)
def create_new_user(org_name,org_phone,org_addr,user_name,user_phone,password):
	msg=[]
	if frappe.db.exists("User Information",user_phone):
		msg.append("Already Registered")
	else:
		user_doc=frappe.new_doc("User Information")
		user_doc.organization_name=org_name
		user_doc.organization_phone_number=org_phone
		user_doc.organization_address=org_addr
		user_doc.user_name=user_name
		user_doc.user_phone_number=user_phone
		user_doc.password=password
		user_doc.save()
		msg.append("Registered Successfully")
	return msg




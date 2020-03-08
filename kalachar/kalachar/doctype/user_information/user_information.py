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
	status=[]
	User_information_doc=frappe.get_doc("User Information",phone_no)
	if password==User_information_doc.password:
		status.append("allowed")
	else:
		status.append("not allowed")
	return status
@frappe.whitelist(allow_guest=True)
def get_dancer_detail(usertype):
	dancers=[]
	dancer_list=frappe.get_all("User Information",filters={'user_type':usertype})
	for dancer in dancer_list:
		category={}
		dancer_doc=frappe.get_doc("User Information",dancer.name)
		category['org_name']=dancer_doc.organization_name
		category['org_addr']=dancer_doc.organization_address
		category['org_phone']=dancer_doc.organization_phone_number
		# for charges in dancer_doc.charging_details:
		# 	if charges.purpose==purpose and charges.dance_type==type_:
		# 		category['timing']=charges.timing
		# 		category['advance_amount']=charges.advance_amount
		# 		category['full_amount']=charges.full_amount
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
@frappe.whitelist(allow_guest=True)
def get_filter_details(category):
	dancers=[]
	dancer_list=frappe.get_all("User Information",filters={'dance_type':category})
	for dancer in dancer_list:
		category={}
		dancer_doc=frappe.get_doc("User Information",dancer.name)
		category['org_name']=dancer_doc.organization_name
		category['org_addr']=dancer_doc.organization_address
		category['org_phone']=dancer_doc.organization_phone_number
		dancers.append(category)
	return dancers

@frappe.whitelist(allow_guest=True)
def get_selected_dancer_details(org_name,org_phone,org_addr):
	dancers=[]
	dancer_list=frappe.get_all("User Information",filters={'organization_name': org_name,'organization_phone_number':org_phone,'organization_address':org_addr})
	for dancer in dancer_list:
		category={}
		dancer_doc=frappe.get_doc("User Information",dancer.name)
		category['user_name']=dancer_doc.user_name
		category['user_phone']=dancer_doc.user_phone_number
		category['details']=''
		for details in dancer_doc.charging_details:
			category['details']+=details.purpose+"- "+details.timing+"- "+"Advance"+":"+" "+str(details.advance_amount)+", "+"Final Amount"+":"+" "+str(details.full_amount)+"."
		dancers.append(category)
	return dancers	


@frappe.whitelist(allow_guest=True)
def get_profile_details(user_phone):
	users=[]
	category={}
	user_doc=frappe.get_doc("User Information",user_phone);
	category['org_name']=user_doc.org_name
	category['org_phone']=user_doc.org_phone
	category['user_name']=user_doc.user_name
	category['user_phone']=user_doc.user_phone_number
	users.append(category)
	return users

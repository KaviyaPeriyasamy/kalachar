# -*- coding: utf-8 -*-
# Copyright (c) 2020, av2l and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class UserInformation(Document):
	pass
@frappe.whitelist(allow_guest=True)
def get_dancer_detail(category):
	dancers=[]
	category_list = frappe.get_all("Category Details")
	for cat in category_list:
		cat_doc = frappe.get_doc("Category Details",cat['name'])
		category={}
		if cat_doc.user_information:
			dancer_doc=frappe.get_doc("User Information",cat_doc.user_information)
			category['org_name']=dancer_doc.organization_name
			category['org_addr']=dancer_doc.organization_address
			category['org_phone']=dancer_doc.user_phone_number
			category['ctiming']=cat_doc.culturals_timing
			category['cadvance_amount']=cat_doc.culturals_advance_amount
			category['cfull_amount']=cat_doc.culturals_full_amount
			category['wtiming']=cat_doc.workshop_timing
			category['wadvance_amount']=cat_doc.workshop_advance_amount
			category['wfull_amount']=cat_doc.workshop_full_amount
			dancers.append(category)
	return dancers

@frappe.whitelist(allow_guest=True)
def create_new_user(data):
	frappe.set_user('Administrator')
	existing_info = frappe.db.get_value('User Information', {'user_phone_number': data['mobile_no']}, 'name')
	user_doc=frappe.get_doc("User Information", existing_info)
	user_doc.organization_name=data['org_name']
	user_doc.organization_address=data['org_address']
	user_doc.name1=data['name1']
	user_doc.user_type = 'Event Organizer'
	if 'dance_category' in data:
		user_doc.user_type = 'Dancer'
		user_doc.account_info = data["bank_type"] + data["bank_details"]
		user_doc.dance_category = data['dance_category']
	user_doc.save()
	return {
			"status": "open"
		}


@frappe.whitelist(allow_guest=True)
def get_profile_details(user_phone):
	users=[]
	category={}
	user_doc=frappe.get_doc("User Information",user_phone);
	category['org_name']=user_doc.organization_name
	category['org_phone']=user_doc.organization_phone_number
	category['user_name']=user_doc.user_name
	category['user_phone']=user_doc.user_phone_number
	users.append(category)
	return users

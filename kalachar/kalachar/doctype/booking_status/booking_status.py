# -*- coding: utf-8 -*-
# Copyright (c) 2020, av2l and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.utils import flt, cstr 

class BookingStatus(Document):
	def validate(self):
		message=get_user_details(self)
		recipient=[self.to_user]
		send_sms(recipient,cstr(message))
def get_user_details(self):
	from_user_doc=frappe.get_doc("User Information",self.from_user)
	to_user_doc=frappe.get_doc("User Information",self.to_user)
	if self.booking_status=='Booking Request':
		message=f"Hello {to_user_doc.user_name}, You have {self.booking_status} from {from_user_doc.user_name} {from_user_doc.user_phone_number} for {self.purpose} with the requesting amount of {self.bargain},{from_user_doc.organization_name},{from_user_doc.organization_address},{from_user_doc.organization_phone_number} Thank You, Have a Nice day!"
	if self.booking_status=='Booking Accepted':
		message=f"Hello {to_user_doc.user_name}, Your {self.booking_status} from {from_user_doc.user_name},{from_user_doc.organization_name},{from_user_doc.organization_address},{from_user_doc.organization_phone_number} Thank You, Have a Nice day!"
	if self.booking_status=='Booking Rejected':
		message=f"Hello {to_user_doc.user_name}, Your {self.booking_status} from {from_user_doc.user_name},{from_user_doc.organization_name},{from_user_doc.organization_address},{from_user_doc.organization_phone_number} Thank You, Have a Nice day!"
	return message
@frappe.whitelist(allow_guest=True)
def send_request(from_user,phone,status,purpose,bargain_amount):
	request=[]
	if from_user and phone and status:
		doc_=frappe.new_doc("Booking Status")
		doc_.from_user=from_user
		doc_.to_user=phone
		doc_.booking_status=status
		doc_.purpose=purpose
		doc_.bargain=bargain_amount
		doc_.save()
		request.append("allowed")
	else:
		request.append("not allowed")
	return request

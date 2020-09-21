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
		send_sms([self.to_user],cstr(get_user_details(self)))
def get_user_details(self):
	message=''
	from_user_doc=frappe.get_doc("User Information",self.from_user)
	to_user_doc=frappe.get_doc("User Information",self.to_user)
	if self.booking_status=='Booking Request':
		message=f"Hello {to_user_doc.user_name}, You have {self.booking_status} from {from_user_doc.user_name} {from_user_doc.user_phone_number} for {self.purpose} with the requesting amount of {self.bargain},{from_user_doc.organization_name},{from_user_doc.organization_address},{from_user_doc.organization_phone_number} on {self.date},timing: {self.time}."
		message+=f"click this link to accept https://kalachar.aerele.in/desk#Form/Booking%20Status/8428849121-8903733423"
		message+="Thank You, Have a Nice day!"
	if self.booking_status=='Booking Accepted':
		message=f"Hello {to_user_doc.user_name}, Your {self.booking_status} from {from_user_doc.user_name},{from_user_doc.organization_name},{from_user_doc.organization_address},{from_user_doc.organization_phone_number} Thank You, Have a Nice day!"
	if self.booking_status=='Booking Rejected':
		message=f"Hello {to_user_doc.user_name}, Your {self.booking_status} from {from_user_doc.user_name},{from_user_doc.organization_name},{from_user_doc.organization_address},{from_user_doc.organization_phone_number} Thank You, Have a Nice day!"
	return message
# @frappe.whitelist(allow_guest=True)
# def send_request(from_user,phone,status,purpose,bargain_amount,date,time):
# 	request=[]
# 	doc_status = frappe.db.get_value("Booking Status", filters={'from_user':from_user, 'to_user':phone, 'date': date},'name')
# 	if not doc_status:
# 		doc_=frappe.new_doc("Booking Status")
# 		doc_.from_user=from_user
# 		doc_.to_user=phone
# 		doc_.booking_status=status
# 		doc_.purpose=purpose
# 		doc_.bargain=bargain_amount
# 		doc_.date=date
# 		doc_.time=time
# 		doc_.save()
# 		request.append("Done")
# 	else:
# 		doc_=frappe.get_doc("Booking Status", doc_status)
# 		doc_.from_user=from_user
# 		doc_.to_user=phone
# 		doc_.booking_status=status
# 		doc_.save()
# 		request.append("Done")
# 	return request


@frappe.whitelist(allow_guest=True)
def send_booking_info(phone_no):
	frappe.set_user("Administrator")
	send_sms([cstr(phone_no)],cstr("Hello Kalainayam, You have got booking request from KIT for culturals with the requesting amount of 8000, on 24-10-2020 for 2 hours."))

@frappe.whitelist(allow_guest=True)
def deny_booking_info(phone_no):
	frappe.set_user("Administrator")
	send_sms([cstr(phone_no)],cstr("Hello, Your booking request declined"))

@frappe.whitelist(allow_guest=True)
def accept_booking_info(phone_no):
	frappe.set_user("Administrator")
	send_sms([cstr(phone_no)],cstr("Hello, Your booking request accepted. Send advance amount to this GPAY UPI ID : kalainayam@oksbi"))
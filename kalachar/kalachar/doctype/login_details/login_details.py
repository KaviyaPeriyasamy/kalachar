# -*- coding: utf-8 -*-
# Copyright (c) 2020, av2l and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import requests
from frappe.utils import time_diff, now_datetime
from frappe.core.doctype.user.user import generate_keys
import secrets

class LoginDetails(Document):
	pass

def set_custom_fields(update=True):
	custom_fields = {
		'User': [
			{
				"fieldname": "login_detail_id",
				"fieldtype": "Link",
				"label": "Login Detail Id",
				"options": "Login Details"
				}
			]
		}
	create_custom_fields(custom_fields, ignore_validate=frappe.flags.in_patch, update=update)


@frappe.whitelist(allow_guest=True)
def login_attempt(mobile_number):
	frappe.set_user(frappe.get_single('Kalachaar App Settings').default_user)
	generated_otp = '{:0>4}'.format(secrets.randbelow(10**4))
	login_detail_doc = frappe.new_doc('Login Details')
	login_detail_doc.update({
		"mobile_number": mobile_number,
		"login_status": 'OTP Generated',
		"generated_otp": generated_otp,
		"generated_time": now_datetime().__str__()[:-7],
	})

	login_detail_doc.save()
	
	response = send_otp(mobile_number, generated_otp)
	json_res = response.json()
	# TODO: handle different errors from MSG91 API and take appropriate actions
	if response.status_code == 200:
		if json_res['type']== 'error':
			frappe.log_error("login detail id: "+login_detail_doc.name+ " | error message: " + json_res['message'] , "Send OTP Error")
			return [{'error_message':'OTP Generation Failed'}]

		if json_res['type'] == 'success':
			return [{"name":login_detail_doc.name}]
	else:
		frappe.log_error("login detail id: "+login_detail_doc.name+ " | code: "+str(response.status_code)+ " | error message: " +  response.text , "Send OTP Error")
		return [{'error_message':'OTP Generation Failed'}]
	return [{"name":login_detail_doc.name}]

@frappe.whitelist(allow_guest = True)
def verify_otp(login_attempt_id, incoming_otp):
	frappe.set_user(frappe.get_single('Kalachaar App Settings').default_user)
	login_attempt_doc = frappe.get_doc("Login Details", {"name": login_attempt_id, "login_status": "OTP Generated"})
	verification_time = now_datetime().__str__()[:-7]
	otp_expiry_limit  = frappe.get_single('Kalachaar App Settings').otp_expiry_limit_in_mins
	max_otp_attempts = frappe.get_single('Kalachaar App Settings').max_otp_attempts

	if not (time_diff(verification_time, login_attempt_doc.generated_time).total_seconds()/60) <= otp_expiry_limit:
		login_attempt_doc.login_status = 'Expired'
		login_attempt_doc.save()
		return {"status":'Expired'}
	if login_attempt_doc.generated_otp == incoming_otp:
		login_attempt_doc.login_status = 'Success'
		login_attempt_doc.save()
		user = frappe.db.get_value('User', {'mobile_no':login_attempt_doc.mobile_number})
		if not user:
			user = create_new_user(login_attempt_doc.mobile_number, login_attempt_id)
		existing_info, existing_info_doc = get_info_from_user(user, True)
		api_secret = generate_keys(user)['api_secret']
		api_key = frappe.db.get_value('User', {'name': user}, "api_key")
		frappe.db.set_value("User", user, "login_detail_id", login_attempt_id)
		return {
			"status":'Success',
			"api_key": api_key,
			"api_secret": api_secret,
			"mobile_no": login_attempt_doc.mobile_number,
		}

	else:
		if len(login_attempt_doc.failed_attempts) == max_otp_attempts:
			login_attempt_doc.login_status = 'Blocked'
			login_attempt_doc.save()
			return {"status":'Maximum Limit Reached'}
		else:
			login_attempt_doc.append('failed_attempts',{'failed_incoming_otp': incoming_otp})
			login_attempt_doc.save()
			return {"status":'Failed'}

def send_otp(mobile_number, generated_otp):
	template_id = frappe.get_single('Kalachaar App Settings').msg91_template_id
	authkey = frappe.get_single('Kalachaar App Settings').msg91_auth_key
	mobile_number = '91'+mobile_number
	url = f"https://api.msg91.com/api/v5/otp/?otp={generated_otp}&authkey={authkey}&mobile={mobile_number}&template_id={template_id}"
	headers = {
		"Content-Type": "application/json"
	}
	response = requests.request("GET", url, headers=headers)
	return response

@frappe.whitelist(allow_guest = True)
def resend_otp(login_attempt_id):
	frappe.set_user(frappe.get_single('Kalachaar App Settings').default_user)
	default_limit = frappe.get_single('Kalachaar App Settings').resend_otp_limit
	mobile_number = '91'+frappe.db.get_value('Login Details', {'name':login_attempt_id}, 'mobile_number')
	authkey = frappe.get_single('Kalachaar App Settings').msg91_auth_key
	login_attempt_doc = frappe.get_doc('Login Details', login_attempt_id)
	login_attempt_doc.resend_count += 1
	login_attempt_doc.save()
	resend_count = login_attempt_doc.resend_count
	if resend_count <= default_limit:
		if resend_count == default_limit:
			url = f"https://api.msg91.com/api/v5/otp/retry?mobile={mobile_number}&authkey={authkey}"
		elif resend_count < default_limit:
			url = f"https://api.msg91.com/api/v5/otp/retry?mobile={mobile_number}&authkey={authkey}&retrytype=text"
		headers = {
			"Content-Type": "application/json"
		}
		response = requests.request("GET", url, headers=headers)
		json_res = response.json()
		if response.status_code == 200:
			if json_res['type'] == 'error':
				frappe.log_error("login attempt id: "+login_attempt_id+" | error message: " + json_res['message'] , "Resend OTP Error")
				return [{"status":"Failed"}]
			if json_res['type'] == 'success':
				return [{"status": "Success"}]
		else:
			frappe.log_error("login attempt id: "+login_attempt_id + " | code: " + str(response.status_code) + " | response: " + response.text , "Resend OTP Error")
			return [{"status":"Failed"}]
	else:
		return [{"status":"Maximum Limit Reached"}]

def create_new_user(mobile_number, login_attempt_id):
	user_doc = frappe.new_doc('User')
	user_doc.update({
		"first_name": mobile_number,
		"email": 'admin+'+mobile_number+'@kalachaar.com',
		"login_detail_id": login_attempt_id,
		"mobile_no": mobile_number,
		"roles":[]
	})
	user_doc.save()
	if user_doc:
		create_user_info(user_doc.name, user_doc.mobile_no)
		return user_doc.name

def create_user_info(user_doc, mobile_no):
	if mobile_no:
		existing_info = frappe.db.get_value('User Information', {'user_phone_number': mobile_no}, 'name')
		if not existing_info:
			new_info = frappe.new_doc('User Information')
			new_info.user = user_doc
			new_info.user_phone_number = mobile_no
			new_info.save()

def get_info_from_user(user, get_as_doc=False):
	if user:
		existing_info = frappe.db.get_value('User Information', {'user': user}, 'name')
		if existing_info:
			if not get_as_doc:
				return existing_info
			existing_info_doc = frappe.get_doc('User Information', existing_info)
			return existing_info, existing_info_doc

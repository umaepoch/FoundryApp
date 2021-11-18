# -*- coding: utf-8 -*-
# Copyright (c) 2021, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import save_file
import base64
import json

class KYC(Document):
	pass

@frappe.whitelist()
def create_file(doc):
	try:
		data = {}
		kyc = json.loads(doc)
		doc_name = kyc['name']
		doctype = kyc['type']
		user_name  = kyc['user']

		# print(kyc['images']['profile'])
		for key, value in kyc['images'].items():
			i = base64.b64decode(value)
			if key == 'profile':
				# print(value)
				sf = save_file(user_name+"_"+key+".png", i, doctype, doc_name)
				data[key] = sf.file_url
			if key == 'adhaar':
				# print(value)
				sf = save_file(user_name+"_"+key+".png", i, doctype, doc_name)
				data[key] = sf.file_url
			if key == 'pan':
				# print(value)
				sf = save_file(user_name+"_"+key+".png", i, doctype, doc_name)
				data[key] = sf.file_url

		return {"SC":data}
	except Exception as ex:
		return{"EX":ex}


@frappe.whitelist()
def set_image_url(profile_url, adhaar_url, pan_url, doc_name, doctype):
	try:
		doc = frappe.get_doc(doctype, doc_name)
		doc.profile_url = profile_url
		doc.adhaar_url = adhaar_url
		doc.pan_url = pan_url
		doc.save()
		if (doc.profile_url and doc.adhaar_url and doc.pan_url):
			return{"SC": 1}
		return {"SC": 0}
	except Exception as ex:
		return{"EX":ex}


		# path = frappe.utils.get_site_path()
		# img = base64.b64decode(image)
#               with open(path+"/public/files/sample.png", "wb") as fh:
#                       fh.write(img)
#               doc = frappe.new_doc("File")
#               doc.file_name = "sample.png"
#               doc.attached_to_name = "abc"
#               doc.attached_to_doctype = "Port Mapping"
#               doc.file_url    = "/files/sample.png"
#               doc.save()

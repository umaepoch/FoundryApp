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
		for img in kyc['images']:
			# i = base64.b64decode(value)
			if "profile" in img.keys():
				sf = save_file(doc_name+".png", i, doctype, doc_name)
				data[key] = sf.file_url
			if "adhaar" in img.keys():
				print(doc_name)
				sf = save_file(doc_name+".png", i, doctype, doc_name)
				data[key] = sf.file_url
			if "pan" in img.keys():
				print(doc_name)
				sf = save_file(doc_name+".png", i, doctype, doc_name)
				data[key] = sf.file_url

		return {"SC":data}
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

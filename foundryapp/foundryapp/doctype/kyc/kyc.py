# -*- coding: utf-8 -*-
# Copyright (c) 2021, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils.file_manager import save_file
import base64

class KYC(Document):
	pass

@frappe.whitelist()
def create_file(image, doc_name, doctype):
        try:
                path = frappe.utils.get_site_path()
                img = base64.b64decode(file)
#               with open(path+"/public/files/sample.png", "wb") as fh:
#                       fh.write(img)
#               doc = frappe.new_doc("File")
#               doc.file_name = "sample.png"
#               doc.attached_to_name = "abc"
#               doc.attached_to_doctype = "Port Mapping"
#               doc.file_url    = "/files/sample.png"
#               doc.save()
                sf = save_file(doc_name+".png", image, doctype, doc_name)
                return {"SC":sf.file_url}
        except Exception as ex:
                return{"EX":ex}

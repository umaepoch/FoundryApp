# -*- coding: utf-8 -*-
# Copyright (c) 2021, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe

class Container(Document):
	pass

@frappe.whitelist()
def fetch_so_details(foreign_buyer, final_destination):
	so_details = []
	try:
		# if show_dispatch_items == '1':
		# 	so_details = frappe.db.sql("""select tso.name, tso.po_no, tso.foreign_buyer_name, tso.final_destination,
		# 							tbi.item_code, tsi.pch_pallet_size, tsi.qty,tso.transaction_date, tsi.delivery_date
		# 							from `tabSales Order Item` as tsi
		# 							join `tabSales Order` as tso on tso.name = tsi.parent
		# 							join `tabBOM` as tb on tsi.item_code = tb.item
		# 							join `tabBOM Item` as tbi on tb.name = tbi.parent
		# 							join `tabItem` as ti on ti.item_code = tbi.item_code
		# 							where ti.pch_made=1 and tso.foreign_buyer_name=%s
		# 							and tso.final_destination=%s
		# 							order by tso.po_no """,(foreign_buyer, final_destination), as_dict=1)
		#
		# elif show_dispatch_items == '0':
		so_details = frappe.db.sql("""select tso.name, tso.po_no, tso.foreign_buyer_name, tso.final_destination,
									tsi.item_code, tsi.pch_pallet_size, tsi.qty, tso.transaction_date, tsi.delivery_date
									from `tabSales Order Item` as tsi
									join `tabSales Order` as tso on tso.name = tsi.parent
									join `tabItem` as ti on ti.item_code = tsi.item_code
									where ti.pch_made=1 and tso.foreign_buyer_name=%s
									and tso.final_destination=%s
									order by tso.po_no,tsi.item_code""",(foreign_buyer, final_destination), as_dict = 1)
		return so_details
	except Exception as ex:
		return ex

@frappe.whitelist()
def validate_container_exist(foreign_buyer, final_destination):
	try:
		not_started = "Not Started"
		worked_upon = "Being Worked Upon"
		cont = frappe.db.sql("""select name from `tabContainer`
								where (`tabContainer`.foreign_buyer=%s and `tabContainer`.final_destination=%s)
								and (`tabContainer`.document_status=%s or `tabContainer`.document_status=%s)""",
							(foreign_buyer, final_destination, not_started, worked_upon), as_dict=1)
		print(cont)
		return cont
	except Exception as ex:
		print(ex)
		return ex

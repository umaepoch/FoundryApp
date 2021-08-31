# -*- coding: utf-8 -*-
# Copyright (c) 2021, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe
import json

class Container(Document):
	pass

@frappe.whitelist()
def fetch_so_details(document, foreign_buyer, final_destination):
	try:
		# date_format = "%d-%m-%Y"
		so_details = frappe.db.sql("""select tso.name, tso.po_no, tso.foreign_buyer_name, tso.final_destination,
									tsi.item_code, tsi.pch_pallet_size, tsi.qty, tsi.quantity_left_in_so,
									tso.transaction_date,
									tsi.delivery_date
									from `tabSales Order Item` as tsi
									join `tabSales Order` as tso on tso.name = tsi.parent
									join `tabItem` as ti on ti.item_code = tsi.item_code
									where ti.pch_made=1 and tso.foreign_buyer_name=%s
									and tso.final_destination=%s
									order by tso.po_no,tsi.item_code""",
									(foreign_buyer, final_destination),
									as_dict = 1)


		if document == 'Sales Order':
			print(" ")
			print("entered condition for sales order report.............")
			print(so_details)
			container = {
			'foreign_buyer': foreign_buyer,
			'final_destination': final_destination,
			'container_details': []
			}

			for sd in so_details:
				child = {
					'so_no': sd.name,
					'item': sd.item_code,
					'pallet_size': sd.pch_pallet_size,
					'so_qty': sd.qty,
					'final_destination': sd.final_destination,
					'customer_po_number': sd.po_no,
					'so_date': sd.delivery_date,
					'initial_delivery_date': sd.transaction_date
				}
				print("child : ", child)
				container['container_details'].append(child)

			# doc = frappe.new_doc('Container')
			# doc.update(outerjson)
			print("Container : ", container)
			print(" ")
			return container

		if document == 'Container':
			return so_details
	except Exception as ex:
		print(ex)
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

@frappe.whitelist()
def get_container_dispatch_items(so_no, item_code, parent):
	try:
		dispatch = frappe.db.sql(""" select tcc.item, tcc.pallet_size,
								tcc.total_quantity_of_item_in_container as quantity_planned_in_container,
								tbi.item_code as dispatch_items,
								tcc.total_quantity_of_item_in_container as quantity
								from `tabContainer Child` as tcc
								join `tabContainer` as tc on tcc.parent = tc.name
								join `tabBOM` as tb on tcc.item =tb.item
								join `tabBOM Item` as tbi on tb.name = tbi.parent
								join `tabItem` as ti on ti.item_code = tbi.item_code
								where (ti.pch_made=1 and tcc.item=%s) and (tcc.so_no=%s and tcc.parent=%s)""",
								(item_code, so_no, parent), as_dict=1)
		return dispatch
	except Exception as e:
		raise


@frappe.whitelist()
def update_so_for_qty(so_no, item, so_qty_left):
	try:
		updated_quantity = 0
		doc = frappe.get_doc('Sales Order', so_no)
		flag = 1
		for d in doc.items:
			if d.item_code == item:
					d.quantity_left_in_so = so_qty_left
					updated_quantity = d.quantity_left_in_so
					flag = 0
		doc.save()
		return {"updated_quantity": updated_quantity}
	except Exception as ex:
		return ex

@frappe.whitelist()
def qty_sum(parent,item):
	sum_of_quantity = frappe.db.sql("""select sum(qty_to_be_filled) as total_qty from `tabContainer Child`
								where parent=%s and item=%s""",
							(parent, item), as_dict=1)
	return sum_of_quantity[0].total_qty

@frappe.whitelist()
def container_details(foreign_buyer,final_destination,so_no,item):
	sum_of_quantity = frappe.db.sql("""select 
	 tcc.so_qty as so_qty
	 from `tabContainer Child` as tcc 
	join `tabContainer` as tc on tcc.parent = tc.name
	where tc.foreign_buyer=%s and tc.final_destination=%s and tcc.so_no=%s and tcc.item=%s""",
							(foreign_buyer,final_destination,so_no,item), as_dict=1)
	print("sum of qty",sum_of_quantity)
	if len(sum_of_quantity)==1:
		return sum_of_quantity[0]['so_qty']
	else:
		print("entered in else")
		sum_of_quantity = frappe.db.sql("""select 
		tcc.qty_left_in_so as so_qty
		from `tabContainer Child` as tcc 
		join `tabContainer` as tc on tcc.parent = tc.name
		where tc.foreign_buyer=%s and tc.final_destination=%s and tcc.so_no=%s and tcc.item=%s""",
						(foreign_buyer,final_destination,so_no,item), as_dict=1)
		print("sum of qty",sum_of_quantity)
		return sum_of_quantity[-len(sum_of_quantity)]['so_qty']
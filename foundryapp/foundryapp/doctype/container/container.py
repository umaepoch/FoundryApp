# -*- coding: utf-8 -*-
# Copyright (c) 2021, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
import frappe
import json

class Container(Document):
	pass

@frappe.whitelist()
def fetch_so_details(foreign_buyer, final_destination, po_no):
	r_data = []
	so_details = []

	try:
		if (foreign_buyer and final_destination and po_no):
			so_details = get_so_foreign_final_po(foreign_buyer, final_destination, po_no)

		if (foreign_buyer and final_destination and (not po_no or po_no.isspace())):
			so_details = get_so_foreign_final(foreign_buyer, final_destination)

		if (foreign_buyer and po_no and (not final_destination or final_destination.isspace())):
			so_details = get_so_foreign_po(foreign_buyer, po_no)

		if (foreign_buyer and (not final_destination or final_destination.isspace()) and (not po_no or po_no.isspace())):
			so_details = get_so_foreign_buyer(foreign_buyer)


		if (len(so_details) > 0):
			# print("details",so_details)
			for d in so_details:
				print("so_no : ",d.name)
				if d.name:
					so_no = d.name
					item = d.item_code
					data = frappe.db.sql("""select so_no,so_qty,
										item,sum(qty_to_be_filled),
										so_qty-sum(qty_to_be_filled) as qty_in_so
										from `tabContainer Child`
										where so_no=%s and item=%s""",
										(so_no, item),as_dict=1)
					print("data : ",data)
					if data[0].qty_in_so is None or data[0].qty_in_so == "":
						r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
										'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
										'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
										'delivery_date':d['delivery_date'],'qty':d['qty'],
										'qty_left_in_so':d['qty']})
					else:
						qty_in_so=data[0].qty_in_so;
						if qty_in_so:
							r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
										'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
										'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
										'delivery_date':d['delivery_date'],'qty':d['qty'],
										'qty_left_in_so':qty_in_so})
			print("r_data",r_data)
		return r_data
	except Exception as ex:
		print(ex)
		return {"Exception": ex}

def get_so_foreign_buyer(foreign_buyer):
	so_details = frappe.db.sql("""select tso.name, tso.po_no,
							tso.foreign_buyer_name, tso.final_destination,
							tsi.item_code,tsi.item_name,tsi.pch_pallet_size,
							tso.transaction_date,
							tsi.delivery_date,
							tsi.qty from `tabSales Order Item` as tsi
							join `tabSales Order` as tso on tso.name = tsi.parent
							join `tabItem` as ti on ti.item_code = tsi.item_code
							where ti.pch_made=1 and tso.foreign_buyer_name=%s
							order by tso.po_no,tsi.item_code""",
							(foreign_buyer),
							as_dict = 1)

	if so_details != None and len(so_details) > 0:
		return so_details
	return ""

def get_so_foreign_final(foreign_buyer, final_destination):
	so_details = frappe.db.sql("""select tso.name, tso.po_no,
								tso.foreign_buyer_name, tso.final_destination,
								tsi.item_code,tsi.item_name,tsi.pch_pallet_size,
								tso.transaction_date,
								tsi.delivery_date,
					 			tsi.qty from `tabSales Order Item` as tsi
					 			join `tabSales Order` as tso on tso.name = tsi.parent
								join `tabItem` as ti on ti.item_code = tsi.item_code
								where ti.pch_made=1 and tso.foreign_buyer_name=%s
								and tso.final_destination=%s
								order by tso.po_no,tsi.item_code""",
								(foreign_buyer, final_destination),
								as_dict = 1)

	if so_details != None and len(so_details) > 0:
		return so_details
	return ""

def get_so_foreign_po(foreign_buyer, po_no):
	so_details = frappe.db.sql("""select tso.name, tso.po_no,
								tso.foreign_buyer_name, tso.final_destination,
								tsi.item_code,tsi.item_name,tsi.pch_pallet_size,
								tso.transaction_date,
								tsi.delivery_date,
					 			tsi.qty from `tabSales Order Item` as tsi
					 			join `tabSales Order` as tso on tso.name = tsi.parent
								join `tabItem` as ti on ti.item_code = tsi.item_code
								where ti.pch_made=1 and tso.foreign_buyer_name=%s
								and tso.po_no=%s
								order by tso.po_no,tsi.item_code""",
								(foreign_buyer, po_no),
								as_dict = 1)

	if so_details != None and len(so_details) > 0:
		return so_details
	return ""

def get_so_foreign_final_po(foreign_buyer, final_destination, po_no):
	so_details = frappe.db.sql("""select tso.name, tso.po_no,
								tso.foreign_buyer_name, tso.final_destination,
								tsi.item_code,tsi.item_name,tsi.pch_pallet_size,
								tso.transaction_date,
								tsi.delivery_date,
					 			tsi.qty from `tabSales Order Item` as tsi
					 			join `tabSales Order` as tso on tso.name = tsi.parent
								join `tabItem` as ti on ti.item_code = tsi.item_code
								where ti.pch_made=1 and tso.foreign_buyer_name=%s
								and tso.final_destination=%s and tso.po_no =%s
								order by tso.po_no,tsi.item_code""",
								(foreign_buyer, final_destination, po_no),
								as_dict = 1)

	if so_details != None and len(so_details) > 0:
		return so_details
	return ""



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
def create_container_dispatch_items(cont_name, qty):
	try:
		# child = json.loads(cont_child)
		print(cont_name)
		outer_json = {
			'total_planned_net_weight_of_container': qty,
			'dispatch_items': []
		}

		dispatch_item = frappe.db.sql("""select tcc.parent, tcc.item, tcc.item_name, tcc.pallet_size,
									tcc.total_quantity_of_item_in_container as quantity_plnd_in_cont,
									tbi.item_code,
									truncate((tcc.total_quantity_of_item_in_container*tbi.qty)/tb.quantity, 0) as quantity
									from `tabContainer Child` as tcc
									join `tabBOM` as tb on tcc.item = tb.item
									join `tabBOM Item` as tbi on tb.name = tbi.parent
									join `tabItem` as ti on ti.item_code = tbi.item_code
									where ti.pch_made=1 and tb.is_default=1 and tbi.docstatus=1 and  tcc.parent=%s
									group by tbi.item_code""",(cont_name), as_dict = 1)

		if (len(dispatch_item) > 0):
			for di in dispatch_item:
				if di['parent']:
					dispatch_json = {
						'parent': di['parent'],
						'invoice_item': di['item'],
						'item_name': di['item_name'],
						'pallet_size': di['pallet_size'],
						'quantity_planned_in_container': di['quantity_plnd_in_cont'],
						'dispatch_item': di['item_code'],
						'quantity': di['quantity']
					}
					outer_json['dispatch_items'].append(dispatch_json)

			doc = frappe.get_doc('Container', cont_name)
			doc.update(outer_json)
			doc.save()
		# print(child['name'])
		# for cd in child['container_details']:
			# print(cd)
			# dispatch_item = get_dispatch(cd['item'])
			# print("got dispatch : ", dispatch_item)

			# for d in dispatch_item:
			# 	if d['item_code']:
			# 		planned_qty = 0
			#
			# 		if 'total_quantity_of_item_in_container' in cd:
			# 			planned_qty = cd['total_quantity_of_item_in_container']
			#
			# 		quantity = planned_qty * d.di_qty / d.in_qty
			# 		dispatch_json = {
			# 			'parent': cd['parent'],
			# 			'invoice_item': cd['item'],
			# 			'item_name': cd['item_name'],
			# 			'pallet_size': cd['pallet_size'],
			# 			'quantity_planned_in_container': planned_qty,
			# 			'dispatch_item': d.item_code,
			# 			'quantity': quantity
			# 		}
			# 		outer_json['dispatch_items'].append(dispatch_json)

		# print(outer_json['dispatch_items'])
		# doc = frappe.get_doc('Container', child['name'])
		# doc.update(outer_json)
		# doc.save()

		# return "success!!" if doc.docstatus == 0 else ""
		return "success!!"
	except Exception as ex:
		print(ex)
		return {"Exception": ex}


def get_dispatch(item):
	dispatch_item = frappe.db.sql("""select tbi.item_code, tbi.item_name, tb.quantity as in_qty, tbi.qty as di_qty  from `tabBOM` as tb
								join `tabBOM Item` as tbi on tb.name = tbi.parent
								join `tabItem` as ti on ti.item_code = tbi.item_code
								where tb.is_default=1 and tbi.docstatus=1 and ti.pch_made=1
								and tb.item=%s""",
								(item), as_dict = 1)

	if dispatch_item != None and len(dispatch_item) > 0:
		return dispatch_item
	return ""



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
def set_child_value(doc_name, name, so_qty_bfr_cont, so_qty_aft_cont, qty):
	try:
		# print(doc_name)
		# print(so_qty_bfr_cont)
		# print(so_qty_aft_cont)
		# print(qty)
		flag = frappe.db.set_value("Container Child", name,
				{
				'so_quantity_not_placed_in_containers_before_this_container': so_qty_bfr_cont,
				'so_quantity_not_placed_in_containers_after_this_container': so_qty_aft_cont,
				'total_quantity_of_item_in_container': qty
						})
		# doc = frappe.get_doc("Container", doc_name)
		# # doc.update()
		# doc.save()

		return "success!!"
	except Exception as ex:
		print(ex)
		return {"Exception": ex}


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

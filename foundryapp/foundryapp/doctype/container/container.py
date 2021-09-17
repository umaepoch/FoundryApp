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
def fetch_so_details_foriegn_buyer(foreign_buyer):
	r_data = []
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
	print("details",so_details)
	for d in so_details:
		print("so_no",d.name)
		so_no=d.name
		item=d.item_code
		data=frappe.db.sql("""select so_no,so_qty,item,sum(qty_to_be_filled),so_qty-sum(qty_to_be_filled) as qty_in_so
		from `tabContainer Child` where so_no='"""+so_no+"""' and item='"""+item+"""'
		""", as_dict=1)
		print("data",data[0].so_qty)
		qty_in_so=0;
		if data[0].qty_in_so is None or data[0].qty_in_so is "" :
			print("enterd in if")
			qty_in_so=data[0].so_qty;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':d['qty']})
		else:
			print("entered in else")
			qty_in_so=data[0].qty_in_so;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':qty_in_so})
	print("r_data",r_data)
	return r_data

@frappe.whitelist()
def fetch_so_details(foreign_buyer, final_destination,po_no):
	r_data = []
	so_details = frappe.db.sql("""select tso.name, tso.po_no,
								tso.foreign_buyer_name, tso.final_destination,
								tsi.item_code,tsi.item_name,tsi.pch_pallet_size,
								tso.transaction_date,
								tsi.delivery_date,
					 			tsi.qty from `tabSales Order Item` as tsi
					 			join `tabSales Order` as tso on tso.name = tsi.parent
								join `tabItem` as ti on ti.item_code = tsi.item_code
								where ti.pch_made=1 and tso.foreign_buyer_name='"""+foreign_buyer+"""'
								and tso.final_destination='"""+final_destination+"""' 
								and po_no in ("""+(po_no)+""")
								order by tso.po_no,tsi.item_code""",
								as_dict = 1)
	print("details",so_details)
	for d in so_details:
		print("so_no",d.name)
		so_no=d.name
		item=d.item_code
		data=frappe.db.sql("""select so_no,so_qty,item,sum(qty_to_be_filled),so_qty-sum(qty_to_be_filled) as qty_in_so
		from `tabContainer Child` where so_no='"""+so_no+"""' and item='"""+item+"""'
		""", as_dict=1)
		print("data",data[0].so_qty)
		qty_in_so=0;
		if data[0].qty_in_so is None or data[0].qty_in_so is "" :
			print("enterd in if")
			qty_in_so=data[0].so_qty;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':d['qty']})
		else:
			print("entered in else")
			qty_in_so=data[0].qty_in_so;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':qty_in_so})
	print("r_data",r_data)
	return r_data

@frappe.whitelist()
def fetch_so_details_po_no(foreign_buyer,po_no):
	r_data = []
	so_details = frappe.db.sql("""select tso.name, tso.po_no,
								tso.foreign_buyer_name, tso.final_destination,
								tsi.item_code,tsi.item_name,tsi.pch_pallet_size,
								tso.transaction_date,
								tsi.delivery_date,
					 			tsi.qty from `tabSales Order Item` as tsi
					 			join `tabSales Order` as tso on tso.name = tsi.parent
								join `tabItem` as ti on ti.item_code = tsi.item_code
								where ti.pch_made=1 and tso.foreign_buyer_name='"""+foreign_buyer+"""'
								and po_no in ("""+(po_no)+""")
								order by tso.po_no,tsi.item_code""",
								as_dict = 1)
	print("details",so_details)
	for d in so_details:
		print("so_no",d.name)
		so_no=d.name
		item=d.item_code
		data=frappe.db.sql("""select so_no,so_qty,item,sum(qty_to_be_filled),so_qty-sum(qty_to_be_filled) as qty_in_so
		from `tabContainer Child` where so_no='"""+so_no+"""' and item='"""+item+"""'
		""", as_dict=1)
		print("data",data[0].so_qty)
		qty_in_so=0;
		if data[0].qty_in_so is None or data[0].qty_in_so is "" :
			print("enterd in if")
			qty_in_so=data[0].so_qty;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':d['qty']})
		else:
			print("entered in else")
			qty_in_so=data[0].qty_in_so;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':qty_in_so})
	print("r_data",r_data)
	return r_data

@frappe.whitelist()
def fetch_so_details_final_foreign(foreign_buyer, final_destination):
	r_data = []
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
	print("details",so_details)
	for d in so_details:
		print("so_no",d.name)
		so_no=d.name
		item=d.item_code
		data=frappe.db.sql("""select so_no,so_qty,item,sum(qty_to_be_filled),so_qty-sum(qty_to_be_filled) as qty_in_so
		from `tabContainer Child` where so_no='"""+so_no+"""' and item='"""+item+"""'
		""", as_dict=1)
		print("data",data[0].so_qty)
		qty_in_so=0;
		if data[0].qty_in_so is None or data[0].qty_in_so is "" :
			print("enterd in if")
			qty_in_so=data[0].so_qty;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':d['qty']})
		else:
			print("entered in else")
			qty_in_so=data[0].qty_in_so;
			r_data.append({'name':d.name,'po_no':d['po_no'],'foreign_buyer_name':d['foreign_buyer_name'],
							'final_destination':d['final_destination'],'item_code':d['item_code'],'item_name':d['item_name'],
							'pch_pallet_size':d['pch_pallet_size'],'transaction_date':d['transaction_date'],
							'delivery_date':d['delivery_date'],'qty':d['qty'],
							'qty_left_in_so':qty_in_so})
	print("r_data",r_data)
	return r_data

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
def get_container_dispatch_items(parent):
	items_data=[]
	items = frappe.db.sql("""select distinct item,
	pallet_size,
	total_quantity_of_item_in_container from `tabContainer Child`
	where parent=%s""",(parent),as_dict=1)
	print("items",items)
	for d in items:
		print("item",d.item)
		item=d.item
		data=frappe.db.sql("""select tbi.item_code as dispatch_items,tbi.item_name as item_name
		from `tabBOM` as tb join `tabBOM Item` as tbi
		on tb.name = tbi.parent join `tabItem` as ti
		on ti.item_code = tbi.item_code where tb.is_default=1 and tbi.docstatus=1 and ti.pch_made=1
		and tb.item='"""+item+"""' """, as_dict=1)
		for item in data:
			items_data.append({'item':d.item,
							'item_name':item.item_name,
							'pch_pallet_size':d.pallet_size,
							'total_quantity_of_item_in_container':d.total_quantity_of_item_in_container,
							'dispatch_items':item.dispatch_items})
	print("items_data",items_data)
	return items_data


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

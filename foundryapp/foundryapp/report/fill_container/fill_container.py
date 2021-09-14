# Copyright (c) 2013, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate, comma_and
from collections import defaultdict
import datetime
import json



def execute(filters=None):
	columns = []
	sum_data = []
	columns = get_columns()
	foreign_buyer = filters.get("foreign_buyer")
	print("foreign_buyer",foreign_buyer)
	container = filters.get("container")
	print("container",container)
	from_scheduled_date = filters.get("from_scheduled_date")
	print("from_scheduled_date",from_scheduled_date)
	to_scheduled_date = filters.get("to_scheduled_date")
	print("to_scheduled_date",to_scheduled_date)
	global data
	global condition
	global warehouse_qty
	container_details = fetching_container_details(filters)
	print("container_details",container_details)

	for cont_dict in container_details:
		sum_data.append([
						cont_dict['parent'],
						cont_dict['foreign_buyer'],
						cont_dict['so_no'],
						cont_dict['so_date'].strftime("%d-%m-%y"),
						cont_dict['initial_delivery_date'].strftime("%d-%m-%y"),
						cont_dict['item'],
						cont_dict['pch_pallet_size'],
						cont_dict['so_qty'],
						cont_dict['customer_po_number'],
						cont_dict['qty_left_in_so'],
						cont_dict['final_destination'],
						cont_dict['qty_to_be_filled'],
						cont_dict['container_warehouse'] if cont_dict['container_warehouse'] else "",
						cont_dict['total_quantity_of_item_in_container'],
						cont_dict['scheduled_date'].strftime("%d-%m-%Y") if cont_dict['scheduled_date'] else "",
						cont_dict['dispatch_items'],
						cont_dict['dispatch_item_qty'],
						cont_dict['dispatch_item_uom'],
						cont_dict['source_warehouse'],
						cont_dict['qty_available_in_source_warehouse']
						])

	return columns, sum_data



def fetching_container_details(filters):
	condition = get_conditions(filters)
	items_data=[]
	items = frappe.db.sql(""" select  tc.foreign_buyer,tcc.so_qty as so_qty,tcc.parent,
	tcc.so_date,tcc.initial_delivery_date, tcc.item,tcc.so_no,
	tcc.pallet_size,tcc.customer_po_number,
	tcc.qty_left_in_so,tcc.final_destination,
	tcc.qty_to_be_filled,tcc.container_warehouse,
	tcc.total_quantity_of_item_in_container,
	tcc.scheduled_date  from `tabContainer Child` as tcc
	join `tabContainer` as tc on tcc.parent = tc.name %s""" % condition, as_dict=1)
	print("items",items)

	for d in items:
		print("item",d.item)
		item=d.item
		total_qty_of_container=d.total_quantity_of_item_in_container
		print("total_qty_of_container",total_qty_of_container)
		data=frappe.db.sql("""select tbi.item_code as dispatch_items,ti.stock_uom,
		tbi.qty,tb.quantity
		from `tabBOM` as tb join `tabBOM Item` as tbi
		on tb.name = tbi.parent join `tabItem` as ti
		on ti.item_code = tbi.item_code where tb.is_default=1 and tbi.docstatus=1 and ti.pch_made=1
		and tb.item='"""+item+"""' """, as_dict=1)
		for dispatch_items in data:
			source_warehouse=frappe.db.get_single_value("FoundryApp Settings", "production_entry_warehouse")
			print("source_warehouse",source_warehouse)
			item_code=dispatch_items.dispatch_items
			print("item_code",item_code)
			warehouse_qty=frappe.db.sql("""select actual_qty
			from `tabBin`
			where item_code='"""+item_code+"""' and warehouse='"""+str(source_warehouse)+"""' """, as_dict=1)
			print("warehouse_details",len(warehouse_qty))
			if len(warehouse_qty)!=0:
				warehouse_qty=warehouse_qty[0]['actual_qty']
			else:
				warehouse_qty=0

		for item in data:
			items_data.append({'parent':d.parent,
							'foreign_buyer':d.foreign_buyer,
							'so_no':d.so_no,
							'so_date':d.so_date,
							'initial_delivery_date':d.initial_delivery_date,
							'item':d.item,
							'pch_pallet_size':d.pallet_size,
							'so_qty':d.so_qty,
							'customer_po_number':d.customer_po_number,
							'qty_left_in_so':d.qty_left_in_so,
							'final_destination':d.final_destination,
							'qty_to_be_filled':d.qty_to_be_filled,
							'container_warehouse':d.container_warehouse,
							'total_quantity_of_item_in_container':d.total_quantity_of_item_in_container,
							'scheduled_date':d.scheduled_date,
							'dispatch_items':item.dispatch_items,
							'dispatch_item_qty':d.total_quantity_of_item_in_container*item.qty/item.quantity,
							'dispatch_item_uom':item.stock_uom,
							'source_warehouse':source_warehouse,
							'qty_available_in_source_warehouse':warehouse_qty
							})
	#print("items_data",items_data)
	return items_data

def fetching_unique_container_details(filters):
	condition = get_conditions(filters)
	items_data=[]
	items = frappe.db.sql("""select  distinct tcc.item,
	tc.foreign_buyer,tcc.parent,
	tcc.pallet_size,tcc.final_destination,
	tcc.container_warehouse,
	tcc.total_quantity_of_item_in_container,
	tcc.scheduled_date  from `tabContainer Child` as tcc
	join `tabContainer` as tc on tcc.parent = tc.name %s""" % condition, as_dict=1)
	print("items",items)

	for d in items:
		print("item",d.item)
		item=d.item
		container_warehouse=d.container_warehouse
		data=frappe.db.sql("""select tbi.item_code as dispatch_items,ti.stock_uom,
		tbi.qty,tb.quantity
		from `tabBOM` as tb join `tabBOM Item` as tbi
		on tb.name = tbi.parent join `tabItem` as ti
		on ti.item_code = tbi.item_code where tb.is_default=1 and tbi.docstatus=1 and ti.pch_made=1
		and tb.item='"""+item+"""' """, as_dict=1)

		for dispatch_items in data:
			item_code=dispatch_items.dispatch_items
			print("item_code",item_code)
			source_warehouse=frappe.db.get_single_value("FoundryApp Settings", "production_entry_warehouse")
			print("source_warehouse",source_warehouse)
			warehouse_qty=frappe.db.sql("""select actual_qty
			from `tabBin`
			where item_code='"""+item_code+"""' and warehouse='"""+str(source_warehouse)+"""' """, as_dict=1)
			print("warehouse_details",len(warehouse_qty))
			if len(warehouse_qty)!=0:
				warehouse_qty=warehouse_qty[0]['actual_qty']
			else:
				warehouse_qty=0

		for item in data:
			items_data.append({'parent':d.parent,
							'foreign_buyer':d.foreign_buyer,
							'item':d.item,
							'pch_pallet_size':d.pallet_size,
							'final_destination':d.final_destination,
							'source_warehouse':source_warehouse,
							'container_warehouse':d.container_warehouse,
							'total_quantity_of_item_in_container':d.total_quantity_of_item_in_container,
							'scheduled_date':d.scheduled_date,
							'dispatch_items':item.dispatch_items,
							'dispatch_item_qty':d.total_quantity_of_item_in_container*item.qty/item.quantity,
							'dispatch_item_uom':item.stock_uom,
							'qty_available_in_source_warehouse':warehouse_qty
							})
	#print("items_data",items_data)
	return items_data

@frappe.whitelist()
def create_invoice_stock_entry_material_trans(filters=None):

	data = fetching_unique_container_details(json.loads(filters))
	print("Data ", data)

	company = frappe.db.get_single_value("Global Defaults", "default_company")

	for sw in data:
		if (sw['qty_available_in_source_warehouse'] < sw['dispatch_item_qty']) or (sw['qty_available_in_source_warehouse'] < sw['total_quantity_of_item_in_container']):
			frappe.throw("Not enought Quantity Available in Source Warehouse")

	if data:
		outerJson = {
		"doctype": "Stock Entry",
		"stock_entry_type": "Material Transfer",
		"company": company,
		"items": []
		}
		index = 1
		for items in data:
			innerJson = {
				"item_code":items['dispatch_items'],
				"s_warehouse":items['source_warehouse'],
				"t_warehouse":items['container_warehouse'],
				"qty":items['total_quantity_of_item_in_container'],
				"uom": items['dispatch_item_uom'],
				"doctype": "Stock Entry Detail"
			}
			# index = index+1 if index < len(data) else index

			outerJson['items'].append(innerJson)
			print("inner",innerJson)
			print("Outer Json",outerJson)
		doc = frappe.new_doc("Stock Entry")
		doc.update(outerJson)
		doc.save()
		print(doc.name)
		return doc.name

def get_columns():
	"""return columns"""
	columns = [
			_("Container Number")+":Link/Container:100",
			_("Foreign Buyer")+"::100",
			_("SO No")+"::100",
			_("SO Date")+"::100",
			_("Initial Delivery Date")+"::100",
			_("Item")+":Link/Item:100",
			_("Pallet Size")+"::100",
			_("SO Qty")+"::100",
			_("Customer PO Number")+"::100",
			_("Qty Left in SO")+"::100",
			_("Port")+"::100",
			_("Qty to be filled")+"::100",
			_("Container Warehouse")+"::100",
			_("Total Quantity of Item in Container")+"::100",
			_("Scheduled Date")+"::100",
			_("Dispatch Item")+"::100",
			_("Dispatch Item Quantity")+"::100",
			_("Dispatch Item UOM")+"::100",
			_("Source Warehouse")+"::100",
			_("Quantity Available in Source Warehouse")+"::100",

			]
	return columns

def get_conditions(filters):
	conditions=""
	if filters.get("foreign_buyer"):
		conditions += 'and  tc.foreign_buyer= %s'  % frappe.db.escape(filters.get("foreign_buyer"), percent=False)

	if filters.get("container"):
		conditions +='and tc.name = %s' % frappe.db.escape(filters.get("container"), percent=False)

	if filters.get("from_scheduled_date"):
		conditions +='and tc.scheduled_date>= %s' % frappe.db.escape(filters.get("from_scheduled_date"), percent=False)

	if filters.get("to_scheduled_date"):
		conditions +='and tc.scheduled_date<= %s' % frappe.db.escape(filters.get("to_scheduled_date"), percent=False)


	print("condition",conditions)
	return conditions
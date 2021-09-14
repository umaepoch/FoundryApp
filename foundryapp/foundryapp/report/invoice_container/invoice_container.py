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
	# print("foreign_buyer",foreign_buyer)
	container = filters.get("container")
	# print("container",container)
	from_scheduled_date = filters.get("from_scheduled_date")
	# print("from_scheduled_date",from_scheduled_date)
	to_scheduled_date = filters.get("to_scheduled_date")
	# print("to_scheduled_date",to_scheduled_date)

	global data
	global condition
	global warehouse_qty
	container_details = fetching_container_details(filters)
	# print("container_details",container_details)

	for cont_dict in container_details:
		sum_data.append([
						cont_dict['parent'],
						cont_dict['foreign_buyer'],
						cont_dict['item'],
						cont_dict['pch_pallet_size'],
						cont_dict['final_destination'],
						cont_dict['container_warehouse'] if cont_dict['container_warehouse'] else "",
						cont_dict['total_quantity_of_item_in_container'],
						cont_dict['scheduled_date'].strftime("%d-%m-%Y") if cont_dict['scheduled_date'] else "",
						cont_dict['dispatch_items'],
						cont_dict['dispatch_item_qty'],
						cont_dict['dispatch_item_uom'],
						cont_dict['qty_available_in_source_warehouse']
						])

	return columns, sum_data



def fetching_container_details(filters):
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
			warehouse_qty=frappe.db.sql("""select actual_qty
			from `tabBin`
			where item_code='"""+item_code+"""' and warehouse='"""+str(container_warehouse)+"""' """, as_dict=1)
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
def create_invoice_stock_entry_manufacture(filters):
	try:
		print("reached function")
		data = fetching_container_details(json.loads(filters))
		company = frappe.db.get_single_value("Global Defaults", "default_company")


		for sw in data:
			if (sw['qty_available_in_source_warehouse'] < sw['dispatch_item_qty']) or (sw['qty_available_in_source_warehouse'] < sw['total_quantity_of_item_in_container']):
				frappe.throw("Not enought Quantity Available in Source Warehouse")

		if data:
			min_index = 1
			max_index = len(data)
			for items in data:
				outerJson_dispatch = {
					"doctype": "Stock Entry",
					"title": "Manufacture",
					"stock_entry_type": "Manufacture",
					"company": company,
					"items": []
				}

				# outerJson_invoice = {
				# 	"doctype": "Stock Entry",
				# 	"title": "Manufacture",
				# 	"stock_entry_type": "Manufacture",
				# 	"company": company,
				# 	"items": []
				# }

				innerJson = {
					"item_code":items['dispatch_items'],
					"s_warehouse":items['container_warehouse'],
					"qty":items['dispatch_item_qty'],
					"uom": items['dispatch_item_uom'],
					"allow_zero_valuation_rate": 1,
					"doctype": "Stock Entry Detail"
				}
				outerJson_dispatch['items'].append(innerJson)
				if min_index < max_index:
					if items['item'] == data[min_index]['item']:
						innerJson_dispatch = {
							"item_code":data[min_index]['dispatch_items'],
							"s_warehouse":data[min_index]['container_warehouse'],
							"qty":data[min_index]['dispatch_item_qty'],
							"uom": data[min_index]['dispatch_item_uom'],
							"allow_zero_valuation_rate": 1,
							"doctype": "Stock Entry Detail"
						}

						innerJson_invoice = {
							"item_code": items['item'],
							"t_warehouse": items['container_warehouse'],
							"qty": items['total_quantity_of_item_in_container'],
							"uom": items['dispatch_item_uom'],
							"allow_zero_valuation_rate": 1,
							"doctype": "Stock Entry Detail"
						}

						outerJson_dispatch['items'].append(innerJson_dispatch)
						outerJson_dispatch['items'].append(innerJson_invoice)
						doc_dispatch = frappe.new_doc("Stock Entry")
						doc_dispatch.update(outerJson_dispatch)
						doc_dispatch.save()
						#doc_dispatch.submit()

						# innerJson_invoice = {
						# 	"item_code": items['item'],
						# 	"t_warehouse": items['container_warehouse'],
						# 	"qty": items['total_quantity_of_item_in_container'],
						# 	"uom": items['dispatch_item_uom'],
						# 	"allow_zero_valuation_rate": 1,
						# 	"doctype": "Stock Entry Detail"
						# }
						# outerJson_invoice['items'].append(innerJson_invoice)
						# doc_invoice =  frappe.new_doc("Stock Entry")
						# doc_invoice.update(outerJson_invoice)
						# doc_invoice.save()
					min_index += 1

			return "success!!!!"
	except Exception as ex:
		print("Exception : ",ex)
		return ex


def get_columns():
	"""return columns"""
	columns = [
			_("Container Number")+":Link/Container:100",
			_("Foreign Buyer")+"::100",
			_("Item")+":Link/Item:100",
			_("Pallet Size")+"::100",
			_("Port")+"::100",
			_("Container Warehouse")+"::100",
			_("Total Quantity of Item in Container")+"::100",
			_("Scheduled Date")+"::100",
			_("Dispatch Item")+"::100",
			_("Dispatch Item Quantity")+"::100",
			_("Dispatch Item UOM")+"::100",
			_("Quantity Available in Container Warehouse")+"::100",

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
	# print("condition",conditions)
	return conditions
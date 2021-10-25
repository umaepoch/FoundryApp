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
	dis_items = frappe.db.sql("""select tdi.parent, tc.foreign_buyer, tdi.invoice_item as item, tdi.pallet_size,
				tc.final_destination, tc.warehouse as container_warehouse, tdi.quantity_planned_in_container as total_quantity_of_item_in_container,
				tc.scheduled_date, tdi.dispatch_item as dispatch_items, tdi.quantity, ti.stock_uom from `tabDispatch Items` as tdi
				join `tabContainer` as tc on tdi.parent = tc.name
				join `tabItem` as ti on tdi.invoice_item = ti.item_code
				%s
				order by tdi.invoice_item""" % get_conditions(filters), as_dict = 1)

	for d in dis_items:
		container_warehouse=d.container_warehouse
		item_code=d.dispatch_items

		# print("item_code",item_code)
		warehouse_qty=frappe.db.sql("""select actual_qty
		from `tabBin`
		where item_code='"""+item_code+"""' and warehouse='"""+str(container_warehouse)+"""' """, as_dict=1)
		# print("warehouse_details",len(warehouse_qty))
		if len(warehouse_qty)!=0:
			warehouse_qty=warehouse_qty[0]['actual_qty']
		else:
			warehouse_qty=0

		items_data.append({'parent':d.parent,
						'foreign_buyer':d.foreign_buyer,
						'item':d.item,
						'pch_pallet_size':d.pallet_size,
						'final_destination':d.final_destination,
						'container_warehouse':d.container_warehouse,
						'total_quantity_of_item_in_container':d.total_quantity_of_item_in_container,
						'scheduled_date':d.scheduled_date,
						'dispatch_items':d.dispatch_items,
						'dispatch_item_qty':d.quantity,
						'dispatch_item_uom':d.stock_uom,
						'qty_available_in_source_warehouse':warehouse_qty
						})
	# print("items_data",items_data)

	return items_data

@frappe.whitelist()
def create_invoice_stock_entry_manufacture(filters):
	try:
		print("reached function")
		data = fetching_container_details(json.loads(filters))
		company = frappe.db.get_single_value("Global Defaults", "default_company")
		status = False
		parent = ""

		for sw in data:
			if (sw['qty_available_in_source_warehouse'] < int(sw['dispatch_item_qty'])) or (sw['qty_available_in_source_warehouse'] < sw['total_quantity_of_item_in_container']):
				frappe.throw("Not Enough Quantity Available in Source Warehouse")

		if data:
			min_index = 1
			max_index = len(data)
			sls_inv_data = []
			for items in data:
				outerJson_dispatch = {
					"doctype": "Stock Entry",
					"title": "Manufacture",
					"stock_entry_type": "Manufacture",
					"company": company,
					"items": []
				}

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
						doc_dispatch.submit()

						parent = items['parent']
						status = True if doc_dispatch.docstatus == 1 else False

					min_index += 1

			flag = create_sales_invoice(status, parent)
			return flag
	except Exception as ex:
		print("Exception : ",ex)
		return "Exception"


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

def create_sales_invoice(status, parent):
	try:
		print("entered creation sales invoice")

		if status and parent:
			cont_doc_invoice = frappe.db.get_list('Container Child',filters={'parent': parent}, fields=['name', 'item', 'so_no', 'qty_to_be_filled'], as_list = True)
			foreign_buyer_name = frappe.db.get_value('Container', {'name': parent}, 'foreign_buyer')
			customer = frappe.db.get_value('Sales Order', {'name': cont_doc_invoice[0][2]}, 'customer')
			warehouse = frappe.db.get_value('Container', {'name': parent}, 'warehouse')

			sls_outer_json = {
				"customer": customer,
				"update_stock":1,
				"set_warehouse":warehouse,
				"foreign_buyer_name":foreign_buyer_name,
				"container_id_number": parent,
				"items": []
			}

			for c in cont_doc_invoice:
				# print(c)
				innerJson = {
								"item_code": c[1],
								"qty": c[3],
								"sales_order":c[2]
							}
				sls_outer_json["items"].append(innerJson)

			if (len(sls_outer_json["items"]) > 0):
				doc_sales_inv = frappe.new_doc('Sales Invoice')
				doc_sales_inv.update(sls_outer_json)
				doc_sales_inv.save()

				return "success!!!!"
	except Exception as ex:
		print(ex)
		return ex


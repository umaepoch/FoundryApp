# Copyright (c) 2013, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns = getColumns()
	data = construct_report()

	if filters.get("committed_production_plan"):
		f_data = []
		for d in data:
			if d[1] == filters.get("committed_production_plan"):
				f_data.append(d)
		return columns, f_data

	return columns, data


def construct_report():
	r_data = frappe.db.sql("""select cmpi.week_ending, cmpi.parent, cmpi.dispatch_item, cmpi.dispatch_item_name,
 						cmpi.production_quantity_committed, cmpi.quantity_in_tonnes
 						from `tabCommitted Production Plan Items` as cmpi
 						join `tabCommitted Production Plan` as cmp on cmpi.parent = cmp.name
 						where cmp.is_active=1
 						order by cmpi.week_ending, cmpi.dispatch_item""", as_dict=1)

	if (len(r_data) > 0):
		data = []
		for r in r_data:
			if r['week_ending']:
				data.append([r['week_ending'].strftime("%d-%m-%Y"),r['dispatch_item'],
						r['dispatch_item_name'], r['production_quantity_committed'], r['quantity_in_tonnes']])

		return data

def getColumns():
	columns = [
		("Week Ending")+"::190",
		("Dispatch Item Code")+"::250",
		("Dispatch Item Name")+"::250",
		("Production Quantity Committed")+"::190",
		("Quantity in Tonnes")+"::190"
	]

	return columns

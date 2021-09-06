# Copyright (c) 2013, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import numpy as np

def execute(filters=None):
	columns = get_columns()
	data = construct_report()
	return columns, data


def get_item_columns():
	item_name = frappe.db.sql("""select tcc.item
								from `tabContainer Child` as tcc
								join `tabContainer` as tc on tcc.parent = tc.name
								group by tcc.item
								order by tcc.item""", as_dict=1)
	return item_name


def get_columns():
	"""return columns"""
	columns = [
		("Scheduled Shipment Date")+"::150",
		("Number of Containers")+"::150",
		("Scheduled Shipment Date")+"::150",
		 ]

	item = get_item_columns()
	if len(item) > 0:
		for i in item:
			columns.append(i.item+"::100")

	columns += [("Total Result")+"::150"]
	return columns


def construct_report():
	rpt = []
	date_format = "%d-%m-%Y"
	query_str = "select tc.scheduled_date"

	columns = get_item_columns()

	if (len(columns) > 0):
		for col in columns:
			query_str += ", if(tcc.item="+"'"+col.item+"'"+", truncate(tcc.total_quantity_of_item_in_container,0), 0) as "+"'"+col.item+"'"
		query_str += "from `tabContainer Child` as tcc join `tabContainer` as tc on tcc.parent = tc.name where tc.scheduled_date=%s order by tc.scheduled_date"


	db_query = frappe.db.sql("""select tc.scheduled_date, count(tc.scheduled_date) as number_of_containers
								from (select tc.name, tc.scheduled_date as scheduled_date
								from `tabContainer` as tc) as tc
								group by tc.scheduled_date
								order by tc.scheduled_date""", as_dict=1)
	if (len(db_query) > 0):
		total = []
		t_res = []
		t_tones = []
		t_cont = 0
		ts_res = 0
		for d in db_query:
			res = []
			data = []
			date = d.scheduled_date
			item = frappe.db.sql(query_str, (date), as_dict=1)
			for i in item:
				del i['scheduled_date']
				items = list(i.values())
				data.append(items)

			sum = list(np.sum(data, axis = 0))
			res.append(list(np.sum(data, axis = 0)))
			ts = list(np.sum(res, axis = 1))
			ts_res += ts[0]
			t_res.append(list(np.sum(data, axis = 0)))
			f_date = date.strftime("%d-%m-%Y")
			sum.insert(0, f_date)
			sum.insert(1, d.number_of_containers)
			t_cont += d.number_of_containers
			sum.insert(2, f_date)
			sum.extend(ts)
			rpt.append(list(sum))

		total.append("Total Result")
		total.append(t_cont)
		total.append("Total Result")
		total.extend(list(np.sum(t_res, axis=0)))
		total.append(ts_res)
		rpt.append(total)
	return rpt

# Copyright (c) 2013, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import itertools
import numpy as np

def execute(filters=None):
	columns = get_columns()
	data = construct_query()
	filter_data = []

	if filters.get("container"):
		result = ["Total Result", "", ""]

		for d in data:
			if d[0] == filters.get("container"):
				filter_data.append(d)
				result.extend(list(itertools.islice(d,3, len(d))))
				filter_data.append(result)

		return columns, filter_data

	return columns, data

def get_columns():
	"""return columns"""
	columns = [
		("Container Number")+"::150",
		("Foreign Buyer")+"::150",
		("Final Destination")+"::150",
		 ]

	item = get_item_columns()
	if len(item) > 0:
		for i in item:
			columns.append(i.absolute_name+"::150")

	columns += [("Total Result")+"::150", ("Total Weight (Tonnes)")+"::150"]
	return columns

def get_item_columns():
	item_name = frappe.db.sql("""select tcc.item, concat(tcc.item,"-", tcc.item_name) as absolute_name
								from `tabContainer Child` as tcc
								join `tabContainer` as tc on tcc.parent = tc.name
								group by tcc.item
								order by tcc.item""", as_dict=1)
	return item_name


def construct_query():
	rpt = []
	query_str = "select tcc.parent"

	columns = get_item_columns()

	if (len(columns) > 0):
		for col in columns:
			query_str += ", if(tcc.item="+"'"+col.item+"'"+", truncate(tcc.total_quantity_of_item_in_container,0), 0) as "+"'"+col.item+"'"
		query_str += "from `tabContainer Child` as tcc join `tabContainer` as tc on tcc.parent = tc.name where tcc.parent=%s order by tcc.parent"

	db_query = frappe.db.sql("""select tcc.parent, tc.foreign_buyer, tc.final_destination, tc.total_planned_net_weight_of_container
								from `tabContainer Child` as tcc
								join `tabContainer` as tc on tcc.parent = tc.name
								group by tcc.parent
								order by tcc.parent""", as_dict=1)

	if (len(db_query) > 0):
		total = ["Total Result", "", ""]
		t_res = []
		ts_res = 0
		t_tone = 0
		for d in db_query:
			res = []
			data = []
			tones = d.total_planned_net_weight_of_container
			cont = d.parent
			item = frappe.db.sql(query_str, (cont), as_dict=1)
			for i in item:
				del i['parent']
				items = list(i.values())
				data.append(items)
			sum = list(np.sum(data, axis = 0))
			res.append(list(np.sum(data, axis = 0)))
			ts = list(np.sum(res, axis = 1))
			# print(ts)
			ts_res += ts[0]
			# print(tones)
			t_tone += tones
			t_res.append(list(np.sum(data, axis=0)))
			sum.insert(0, cont)
			sum.insert(1, d.foreign_buyer)
			sum.insert(2, d.final_destination)
			sum.extend(ts)
			# print(sum)
			sum.append(tones)
			rpt.append(list(sum))
		total.extend(list(np.sum(t_res, axis=0)))
		total.append(ts_res)
		total.append(t_tone)
		rpt.append(total)

	return rpt

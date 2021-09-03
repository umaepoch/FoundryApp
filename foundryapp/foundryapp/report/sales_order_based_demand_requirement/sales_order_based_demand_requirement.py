# Copyright (c) 2013, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import itertools

def execute(filters=None):
	columns = get_columns()
	show = filters.get("show_dispatch_items")
	week = ""
	day_of_week = {'Sunday': '1', 'Monday': '2', 'Tuesday': '3',
	 				'Wednesday': '4', 'Thursday': '5', 'Friday': '6', 'Saturday': '7'}
	foundry_settings = frappe.get_doc('FoundryApp Settings')

	for k in day_of_week.keys():
		if foundry_settings.weekly_planning_cycle_ends_on == k:
			print("weeek :",k," value :",day_of_week[k])
			week = day_of_week[k]

	wfw = get_total_weight_for_week(show, week)
	rpt = get_report(show, week)
	data = construct_report(wfw, rpt)
	return columns, data

# fetches the delivery_date, items, sum_quantiy, weight_per_unit, total_weight.
def get_report(sdi, week):
	r_data = []

	if sdi == 1:
		r_data = frappe.db.sql("""select date_sub(date(tsi.delivery_date), interval dayofweek(tsi.delivery_date)-%s day) as delivery_date,
							tbi.item_code, sum(truncate((tsi.qty*tbi.qty)/tb.quantity, 0)) as sum_quantiy,
							ti.weight_per_unit,((sum(tsi.qty)*ti.weight_per_unit)/1000) as total_weight
							from `tabSales Order Item` as tsi
							join `tabSales Order` as tso on tso.name = tsi.parent
							join `tabBOM` as tb on tsi.item_code = tb.item
							join `tabBOM Item` as tbi on tb.name = tbi.parent
							join `tabItem` as ti on ti.item_code = tbi.item_code
							where ti.pch_made=1 and tb.is_default=1 and tbi.docstatus=1
							group by tbi.item_code, delivery_date
							order by delivery_date, tbi.item_code""",(week), as_dict=1)

	if sdi is None:
		r_data = frappe.db.sql("""select date_sub(date(tsi.delivery_date), interval dayofweek(tsi.delivery_date)-%s day) as delivery_date,
							tsi.item_code, sum(tsi.qty) as sum_quantiy, ti.weight_per_unit, ((sum(tsi.qty)*ti.weight_per_unit)/1000) as total_weight
							from `tabSales Order Item` as tsi
							join `tabSales Order` as tso on tso.name = tsi.parent
							join `tabItem` as ti on ti.item_code = tsi.item_code
							where ti.pch_made=1
							group by delivery_date, tsi.item_code
							order by delivery_date, tsi.item_code""",(week), as_dict = 1)
	return r_data

# fetches the sum of weights for a week.
def get_total_weight_for_week(sdi, week):
	wfw_data =[]

	if sdi == 1:
		wfw_data = frappe.db.sql("""select twfw.delivery_date, sum(twfw.total_weight) as total_weight_for_week
								from (
								select date_sub(date(tsi.delivery_date), interval dayofweek(tsi.delivery_date)-%s day) as delivery_date, tbi.item_code,
								sum(tsi.qty) as sum_quantiy, ti.weight_per_unit, ((sum(tsi.qty)*ti.weight_per_unit)/1000) as total_weight
								from `tabSales Order Item` as tsi
								join `tabBOM` as tb on tb.item = tsi.item_code
								join `tabBOM Item` as tbi on tb.name = tbi.parent
								join `tabItem` as ti on ti.item_code = tbi.item_code
								where ti.pch_made=1 and tb.is_default=1 and tbi.docstatus=1
								group by delivery_date, tbi.item_code) as twfw
								group by twfw.delivery_date""",(week), as_dict=1)

	if sdi is None:
		wfw_data = frappe.db.sql("""select twfw.delivery_date, sum(twfw.total_weight) as total_weight_for_week
								from (
								select date_sub(date(tsi.delivery_date), interval dayofweek(tsi.delivery_date)-%s day) as delivery_date, tsi.item_code,
								sum(tsi.qty) as sum_quantiy, ti.weight_per_unit, ((sum(tsi.qty)*ti.weight_per_unit)/1000) as total_weight
								from `tabSales Order Item` as tsi
								join `tabSales Order` as tso on tso.name = tsi.parent
								join `tabItem` as ti on ti.item_code = tsi.item_code
								where ti.pch_made=1
								group by delivery_date, tsi.item_code) as twfw
								group by twfw.delivery_date""",(week), as_dict = 1)

	return wfw_data

# constructs the report based on delivery_date for total_weight_for_week
def construct_report(w_data, r_data):
	report = []
	t_res = "Total result"
	res_twfw = 0
	res_sqty = 0
	res_tw = 0
	index = 0

	# constructs the report and total result.
	for wd in w_data:
		res_twfw += wd['total_weight_for_week']
		for rd in r_data:
			if wd['delivery_date'] == rd['delivery_date']:
				res_tw += rd['total_weight']
				res_sqty += rd['sum_quantiy']
				report.append([rd['delivery_date'].strftime("%d-%m-%y"),rd['item_code'],rd['sum_quantiy'],
								rd['weight_per_unit'],rd['total_weight'],""])
				index += 1
		if index >= 0:
			datum = list(itertools.islice(report[index-1],0,len(report[index-1])-1))
			datum.append(wd['total_weight_for_week'])
			# print("index",(index-1)," :",datum)
			report[index-1] = datum
			print(report[index-1])
	report.append([t_res,"",res_sqty,"",round(res_tw,3),round(res_twfw,3)])
	print(report)
	return report


def get_columns():
	"""return columns"""
	columns = [
		("Delivery Date")+"::200",
		("Dispatch Item/Invoice Item")+"::200",
		("Sum - Quantity")+"::160",
		("Weight (Kg)")+"::160",
		("Total Weight (Tons)")+"::160",
		("Total Weight for week")+"::160",
		 ]
	return columns
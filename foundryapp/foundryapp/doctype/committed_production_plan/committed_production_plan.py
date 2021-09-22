# -*- coding: utf-8 -*-
# Copyright (c) 2021, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe.model.document import Document

class CommittedProductionPlan(Document):
	pass

@frappe.whitelist()
def fetch_cmp_items(week_end_date):
	try:
		cmp_items = []
		foundry_settings = frappe.get_doc('FoundryApp Settings')
		week = ""
		day_of_week = {'Sunday': '1', 'Monday': '2', 'Tuesday': '3',
		 				'Wednesday': '4', 'Thursday': '5', 'Friday': '6', 'Saturday': '7'}
		index = 0

		for k in day_of_week.keys():
			if foundry_settings.weekly_planning_cycle_ends_on == k:
				week = day_of_week[k]

		dispatch = frappe.db.sql("""select tbi.item_code, tbi.item_name
								from `tabBOM` as tb
								join `tabBOM Item` as tbi on tb.name = tbi.parent
								join `tabItem` as ti on ti.item_code = tbi.item_code
								where tb.is_default=1 and tbi.docstatus=1 and ti.pch_made=1
								order by tbi.item_code""", as_dict = 1)
		if (len(dispatch) > 0):
			for d in dispatch:
				if d['item_code']:
					items = frappe.db.sql("""select di.item_code, di.item_name, di.so_requirement, ROUND((di.so_requirement/6), 3) as avg_prod_req_per_day
									from (select tbi.item_name, tbi.item_code, sum(truncate((tsi.qty*tbi.qty)/tb.quantity, 0)) as so_requirement
									from `tabSales Order Item` as tsi
									join `tabSales Order` as tso on tso.name = tsi.parent
									join `tabBOM` as tb on tsi.item_code = tb.item
									join `tabBOM Item` as tbi on tb.name = tbi.parent
									join `tabItem` as ti on ti.item_code = tbi.item_code
									where ti.pch_made=1 and tb.is_default=1 and
									date_sub(date(tsi.delivery_date), interval dayofweek(tsi.delivery_date)-%s day) = %s and
									tbi.item_code=%s
									group by tbi.item_code
									order by tbi.item_code) as di""",(week, week_end_date, d['item_code']), as_dict = 1)

					if (len(items) > 0):
						for i in items:
							if i['item_code']:
								cont_req = frappe.db.sql("""select di.dispatch_item, cont_req, ROUND((di.cont_req/6), 3) as avg_prod_req_per_day_cont
													from (
													select dispatch_item, sum(quantity) as cont_req from `tabDispatch Items`
													where dispatch_item =%s
													group by dispatch_item
													order by dispatch_item) as di""",(i['item_code']), as_dict = 1)

								if (len(cont_req) > 0):
									for c in cont_req:
										if c['dispatch_item'] == i['item_code']:
											i['cont_requirement'] = c['cont_req']
											i['avg_prod_req_per_day_cont'] = c['avg_prod_req_per_day_cont']
							cmp_items.append(i)
					if (len(items) == 0):
						i_json = {
							"item_code": d['item_code'],
							"item_name": d['item_name']
						}
						cmp_items.append(i_json)

		return cmp_items if (len(cmp_items) > 0) else ""
	except Exception as ex:
		print(ex)
		return {"Exception": ex}



@frappe.whitelist()
def check_for_active_cmp(week_start_date, week_end_date):
	# doc = []
	try:
		exists = frappe.db.sql("""select name, week_start_date, week_end_date, is_active from `tabCommitted Production Plan`
								where week_start_date=%s and week_end_date=%s and is_active=1""",(week_start_date, week_end_date), as_dict=1)

		if (len(exists) > 0):
			for e in exists:
				if e.week_start_date and e.week_end_date:
					return {"name": e.name,
							"week_start_date": e.week_start_date.strftime("%d-%m-%Y"),
							"week_end_date": e.week_end_date.strftime("%d-%m-%Y"),
							"is_active": e.is_active}
			# return doc

		# doc.append({"is_active": 0})
		return {"is_active": 0}
	except Exception as ex:
		print(ex)
		return {"Exception": ex}



@frappe.whitelist()
def duplicate_active_doc(cur_doc):
	try:
		doc = frappe.get_doc("Committed Production Plan", cur_doc)

		if doc.name:
			outer_json = {
				"doctype": doc.doctype,
				"week_start_date": doc.items[0].start_date,
				"week_end_date": doc.items[0].week_ending,
				"is_active": 1,
				"items": []
			}

			if doc.items:
				for i in doc.items:
					inner_json = {
						"start_date": i.start_date,
						"week_ending": i.week_ending,
						"dispatch_item": i.dispatch_item,
						"dispatch_item_name": i.dispatch_item_name,
						"production_quantity_committed": i.production_quantity_committed,
						"quantity_in_tonnes": i.quantity_in_tonnes,
						"average_production_per_day_units": i.average_production_per_day_units,
						"average_production_per_day_tonnes": i.average_production_per_day_tonnes,
						"so_requirement": i.so_requirement,
						"average_production_required_per_day": i.average_production_required_per_day,
						"container_plan_requirement": i.container_plan_requirement,
						"average_production_required_per_day_container": i.average_production_required_per_day_container
					}
					outer_json['items'].append(inner_json)

			doc.is_active = 0
			doc.save()
			new_doc = frappe.new_doc(doc.doctype)
			new_doc.update(outer_json)
			new_doc.save()

			return {"name": new_doc.name}
	except Exception as ex:
		print(ex)
		return {"Exception": ex}

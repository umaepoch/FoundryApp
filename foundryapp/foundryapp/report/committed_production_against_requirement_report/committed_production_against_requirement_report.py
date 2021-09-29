# Copyright (c) 2013, yashwanth and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime

def execute(filters=None):
	columns = getColumns()
	data = construct_report(filters.get("scheduled_date"))

	return columns, data


def construct_report(filters):
	r_data = []

	cum_so_rqd = 0
	cum_pln_disp = 0
	cum_uo_dlv = 0
	cum_prod_com = 0
	dispatch = get_dispatch()
	data = get_production_plan()

	if len(data) > 0 and len(dispatch) > 0:
		for i in dispatch:
			for d in data:

				if i['dispatch_item'] == d['item_code']:
					cum_so_rqd += d['so_requirement']
					cum_pln_disp += d['planned_dispatch']
					cum_uo_dlv += d['under/over_delivery']
					cum_prod_com += d['committed_production']

					data[data.index(d)]['cum_so'] = cum_so_rqd
					data[data.index(d)]['cum_dis'] = cum_pln_disp
					data[data.index(d)]['cum_uo'] = cum_uo_dlv
					data[data.index(d)]['cum_prod'] = cum_prod_com
					data[data.index(d)]['cum_shrt'] = cum_prod_com - cum_pln_disp

		cum_so_rqd = 0
		cum_prod_com = 0
		cum_uo_dlv = 0
		cum_pln_disp = 0

		if filters:
			date = datetime.datetime.strptime(filters, '%Y-%m-%d').strftime('%d-%m-%Y')
			for d in data:
				if d['scheduled_shipment_date'] == date:
					r_data.append([d['scheduled_shipment_date'], d['item_code'], d['item_name'],
								d['concat'], d['so_requirement'], d['planned_dispatch'], d['under/over_delivery'],
								d['cum_so'], d['cum_dis'], d['cum_uo'], d['committed_production'],
								d['shortage/excess_production'], d['cum_prod'], d['cum_shrt']])

		if filters is None:
			for d in data:
				r_data.append([d['scheduled_shipment_date'], d['item_code'], d['item_name'],
							d['concat'], d['so_requirement'], d['planned_dispatch'], d['under/over_delivery'],
							d['cum_so'], d['cum_dis'], d['cum_uo'], d['committed_production'],
							d['shortage/excess_production'], d['cum_prod'], d['cum_shrt']])
	return r_data



def getColumns():
	columns = [
		("Scheduled Shipment Date")+"::150",
		("Dispatch Item Code")+"::150",
		("Dispatch Item Name")+"::150",
		("Concat")+"::150",
		("SO Requirement")+"::50",
		("Planned Dispatch")+"::50",
		("Under/Over Delivery")+"::50",
		("Cumulative for the Week - SO Required")+"::50",
		("Cumulative for the Week - Planned Dispatch")+"::50",
		("Cumulative for theWeek - Under/Over Delivery")+"::50",
		("Committed Prodction")+"::50",
		("Shortage/Excess Production")+"::50",
		("Cumulative Production Comittment")+"::50",
		("Cumulative Shortage/Excess Production")+"::50"
	]

	return columns

def get_production_plan():
	data = []
	cmp_details =  frappe.db.sql("""select cmpi.week_ending, cmpi.dispatch_item, cmpi.dispatch_item_name, concat(datediff(cmpi.week_ending, '1900-01-01') + 2,cmpi.dispatch_item) as date_serial_number,
								cmpi.so_requirement, cmpi.container_plan_requirement ,cmpi.production_quantity_committed, cmpi.quantity_in_tonnes
								from `tabCommitted Production Plan Items` as cmpi
								join `tabCommitted Production Plan` as cmp on cmpi.parent = cmp.name
								where cmp.is_active=1
								order by cmpi.week_ending, cmpi.dispatch_item""", as_dict = 1)

	if cmp_details != None and (len(cmp_details) > 0):
		for cmp in cmp_details:
			if cmp['week_ending']:
				cmp_json = {
					'scheduled_shipment_date' : cmp['week_ending'].strftime("%d-%m-%Y"),
					'item_code' : cmp['dispatch_item'],
					'item_name' : cmp['dispatch_item_name'],
					'concat' : cmp['date_serial_number'],
					'so_requirement' : cmp['so_requirement'],
					'planned_dispatch': cmp['container_plan_requirement'],
					'under/over_delivery': cmp['container_plan_requirement'] - cmp['so_requirement'],
					'committed_production': cmp['production_quantity_committed'],
					'shortage/excess_production': cmp['production_quantity_committed'] - cmp['container_plan_requirement']
				}

				data.append(cmp_json)
	return data



def get_dispatch():
	dispatch = frappe.db.sql("""select dispatch_item from `tabCommitted Production Plan Items`
							group by dispatch_item
							order by dispatch_item""", as_dict = 1)

	if dispatch != None and (len(dispatch) > 0):
		return dispatch
	else:
		return []

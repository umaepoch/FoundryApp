# Copyright (c) 2013, Epoch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime

def execute(filters=None):
	columns = get_columns()
		
	rpt = get_report()
	data = construct_report(rpt)
	return columns, data

def get_report():
	r_data = frappe.db.sql("""select tso.name,date_sub(date(tsi.delivery_date), 
						interval dayofweek(tsi.delivery_date)day) as delivery_date,
						concat(datediff(tsi.delivery_date,'1900-01-01') + 2,tsi.item_code) as concat,
						tso.po_no, tso.foreign_buyer_name, tso.final_destination, tsi.item_code,
						tsi.pch_pallet_size,tsi.qty as qty from `tabSales Order Item` as tsi 
						join `tabSales Order` as tso on tso.name = tsi.parent 
						join `tabItem` as ti on ti.item_code = tsi.item_code where 
						ti.pch_made=1 order by tsi.delivery_date,tsi.item_code""", as_dict = 1)
	return r_data

def construct_report(r_data):
	filterData=[]
	l = []
	index = -1
	p = 0
	fetchedIndex = -1
	for data in r_data:
		index = -1
		for f_data in filterData:
			index = index + 1
			if (f_data[1] == data['item_code'] and f_data[0] == data['delivery_date'].strftime('%d-%m-%Y')):
				print("date",data['delivery_date'].strftime('%d-%m-%Y'))
				fetchedIndex = index
				break
			else:
				fetchedIndex = -1
		if(fetchedIndex == -1):
			if(data['pch_pallet_size'] is not None):
				pal = (float(data['pch_pallet_size']))
			else:
				pal = 0
			filterData.append([(data['delivery_date'].strftime('%d-%m-%Y')),data['item_code'],data['concat'],data['qty'],data['pch_pallet_size'],0,data['qty'],data['pch_pallet_size']-pal,0]);
			#filterData[fetchedIndex][2] = data['delivery_date'].strftime("%d-%m-%y") + data['item_code']
		else:
			filterData[fetchedIndex][3] = filterData[fetchedIndex][3] + data['qty']
		if(data['pch_pallet_size'] is not None):
			p = (float(data['pch_pallet_size']))
			filterData[fetchedIndex][4]= filterData[fetchedIndex][3] - p
			filterData[fetchedIndex][5] = filterData[fetchedIndex][4] - filterData[fetchedIndex][3]
		else:
			filterData[fetchedIndex][4]=filterData[fetchedIndex][3]

	fd_data = []
	index = -1
	fetchedIndex  = -1
	for i in filterData:
		index = index + 1
		index1 = -1
		fetchedIndex1 = -1
		for f in fd_data:
			index1 = index1 + 1
			if(f[0] == i[1]):
				fetchedIndex1 = index1
				break
			else:
				fetchedIndex1 = -1
		if(fetchedIndex1 != -1):
			filterData[index][6] = 	filterData[index][3] + fd_data[fetchedIndex1][2]
			print("if - dv",fd_data[fetchedIndex1][2])
			filterData[index][7] = 	filterData[index][4] + fd_data[fetchedIndex1][3] 
			print("filterData[index][7]",filterData[index][7])
			fd_data[fetchedIndex1][2] = filterData[index][6]
			fd_data[fetchedIndex1][3] = filterData[index][7]
			filterData[index][8]=filterData[index][7]-filterData[index][6]
		else:
			fd_data.append([i[1],i[2],i[3],i[4]])
			filterData[index][6]=fd_data[fetchedIndex1][2]
			filterData[index][7] = 	filterData[index][4]
			filterData[index][8]=filterData[index][7]-filterData[index][6]
			print("else - dv",fd_data[fetchedIndex1][2])
	
	return filterData

def get_columns():
	"""return columns"""
	columns = [
		("Scheduled Shipment Date")+"::100",
		("Dispatch Item")+"::100",
		("Concat")+"::70",
		("SO Requirement")+":50",
		("Planned Dispatch")+":50",
		("Under/Over Delivert")+":50",
		("Cumulative for the Week - SO Required")+":50",
		("Cumulative for the Week - Planned Dispatch")+":50",
		("Cumulative for theWeek - Under/Over Delivery")+":50" ]
	return columns
// Copyright (c) 2016, yashwanth and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order Based Demand Requirement"] = {
	"filters": [
		{
			"fieldname": "show_dispatch_items",
			"label": __("Show Dispatch Items"),
			"fieldtype": "Check"
		}
		// {
		// 	"fieldname": "foreign_buyer",
		// 	"label": __("Foreign Buyer"),
		// 	"fieldtype": "Link",
		// 	"options": "Customer"
		// },
		// {
		// 	"fieldname": "final_destination",
		// 	"label": __("Final Destination"),
		// 	"fieldtype": "Link",
		// 	"options": "Port Of Dispatch"
		// }
	],
	onload: function(report) {
		report.page.add_inner_button(__("Sales Order Report"), function() {
			frappe.set_route('query-report', 'Sales Order Container Planning Report')
		});
	}
};
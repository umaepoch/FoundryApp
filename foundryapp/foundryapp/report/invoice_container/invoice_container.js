// Copyright (c) 2016, yashwanth and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Invoice Container"] = {
	"filters": [

		{
			"fieldname": "foreign_buyer",
			"label": __("Foreign Buyer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "container",
			"label": __("Container"),
			"fieldtype": "Link",
			"options": "Container"
		},
		{
			"fieldname": "from_scheduled_date",
			"label": __("From Scheduled Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_scheduled_date",
			"label": __("To Scheduled Date"),
			"fieldtype": "Date"
		},

	],
	onload: function(report) {
		let doc = frappe.query_report.report_name
		report.page.add_inner_button(__("Invoice Container"), function() {
			if (frappe.query_report.get_filter_value('container')) {
				var filter = {
					'foreign_buyer': frappe.query_report.get_filter_value('foreign_buyer') ? frappe.query_report.get_filter_value('foreign_buyer') : '',
					'container': frappe.query_report.get_filter_value('container') ? frappe.query_report.get_filter_value('container') : '',
					'from_scheduled_date': frappe.query_report.get_filter_value('from_scheduled_date') ? frappe.query_report.get_filter_value('from_scheduled_date') : '',
					'to_scheduled_date': frappe.query_report.get_filter_value('to_scheduled_date') ? frappe.query_report.get_filter_value('to_scheduled_date') : '',
					'source_warehouse': frappe.query_report.get_filter_value('source_warehouse') ? frappe.query_report.get_filter_value('source_warehouse') : ''
				}
				var doc_name = get_invoice_container_stock(JSON.stringify(filter))
				if (doc_name) {
					console.log(doc_name)
					frappe.set_route("List/Sales Invoice/")
				}
			} else {
				frappe.throw(__("Please Select The Container"))
			}
		})
	}
};

function get_invoice_container_stock(filters) {
	let form
	frappe.call({
		method: 'foundryapp.foundryapp.report.invoice_container.invoice_container.create_invoice_stock_entry_manufacture',
		args: {
			filters: filters
		},
		async: false,
		callback: function(r) {
			if (r.message) {
				console.log(r.message)
				form = r.message
			}
		}
	})
	return form
}
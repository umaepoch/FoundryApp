// Copyright (c) 2016, yashwanth and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Fill Container"] = {
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
		}

	],
	onload: function(report) {
		let doc = frappe.query_report.report_name
		report.page.add_inner_button(__("Fill Container"), function() {
			if (frappe.query_report.get_filter_value('container')) {
				var filter = {
					'foreign_buyer': frappe.query_report.get_filter_value('foreign_buyer') ? frappe.query_report.get_filter_value('foreign_buyer') : '',
					'container': frappe.query_report.get_filter_value('container') ? frappe.query_report.get_filter_value('container') : '',
					'from_scheduled_date': frappe.query_report.get_filter_value('from_scheduled_date') ? frappe.query_report.get_filter_value('from_scheduled_date') : '',
					'to_scheduled_date': frappe.query_report.get_filter_value('to_scheduled_date') ? frappe.query_report.get_filter_value('to_scheduled_date') : '',
					'source_warehouse': frappe.query_report.get_filter_value('source_warehouse') ? frappe.query_report.get_filter_value('source_warehouse') : ''
				}
				var doc_name = get_invoice_container_stock_material_trans(JSON.stringify(filter))
				if (doc_name) {
					console.log(doc_name)
					frappe.set_route("Form/Stock Entry/"+doc_name)
				}
			} else {
				frappe.throw(__("Please Select The Container"))
			}
		});
	}
};

function get_invoice_container_stock_material_trans(filters) {
	let form
	frappe.call({
		method: 'foundryapp.foundryapp.report.fill_container.fill_container.create_invoice_stock_entry_material_trans',
		args: {
			filters: filters
		},
		async: false,
		callback: function(r) {
			if (r.message) {
				console.log(typeof r.message)
				form = r.message
			}
		}
	})
	return form
}
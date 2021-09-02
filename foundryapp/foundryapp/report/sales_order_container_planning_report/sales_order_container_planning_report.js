// Copyright (c) 2016, yashwanth and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order Container Planning Report"] = {
	"filters": [
		{
			"fieldname": "show_dispatch_items",
			"label": __("Show Dispatch Items"),
			"fieldtype": "Check"
		},
		{
			"fieldname": "foreign_buyer",
			"label": __("Foreign Buyer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "final_destination",
			"label": __("Final Destination"),
			"fieldtype": "Link",
			"options": "Ports"
		}
	],
	onload: function(report) {
		let doc = frappe.query_report.report_name
		report.page.add_inner_button(__("Make Sales Order Based Demand Requirement"), function() {
			frappe.set_route('query-report', 'Sales Order Based Demand Requirement')
		});
		report.page.add_inner_button(__("Make Container Plan"), function() {
			// console.log(frappe.query_report.get_filter_value("show_dispatch_items"))

			var d = new frappe.ui.Dialog({
				title: __("Select Foreign Buyer and Final Destination"),
				'fields': [
					{
						"fieldname": "foreign_buyer",
						"label": __("Foreign Buyer"),
						"fieldtype": "Link",
						"options": "Customer",
        				"reqd": 1,
					},
					{
						"fieldname": "final_destination",
						"label": __("Final Destination"),
						"fieldtype": "Link",
						"options": "Ports",
        				"reqd": 1,
					},
				],
				primary_action: function(values){
					d.hide()
					var foreign_buyer = values.foreign_buyer
					var final_destination = values.final_destination
					// var cont = get_new_container(foreign_buyer, final_destination, doc)
					// console.log("container details : ",cont)
					frappe.set_route("Form/Container/New Container",{"foreign_buyer": foreign_buyer, "final_destination": final_destination})
					// var msg = check_for_existing(foreign_buyer, final_destination)
					// if (msg.length > 0) {
					// 	var existing = ""
	        //   msg.forEach((cont)=> {
	        //     existing += cont["name"]+" "
	        //   })
					// 	frappe.confirm(`The Following Container Plans ${existing} exist for this combination that has not been Finalized yet. Do you want to work with that Document?`,
	        //     () => {
	        //       // action to perform if Yes is selected
	        //     }, () => {
	        //       // action to perform if No is selected
					// 			frappe.set_route("Form/Container/New Container",{"foreign_buyer": foreign_buyer, "final_destination": final_destination})
	        //     })
	        // }
					// if (msg.length == 0) {
					// }
				}
			});
			if (frappe.query_report.get_filter_value("foreign_buyer")) {
				// console.log(frappe.query_report.get_filter_value("foreign_buyer"))
				d.fields_dict.foreign_buyer.set_value(frappe.query_report.get_filter_value("foreign_buyer"))
			}
			if (frappe.query_report.get_filter_value("final_destination")) {
				// console.log(frappe.query_report.get_filter_value("final_destination"))
				d.fields_dict.final_destination.set_value(frappe.query_report.get_filter_value("final_destination"))
			}
			d.show()
		});
	}
};

function get_new_container(foreign_buyer, final_destination, doc) {
	let cont_details;
	frappe.call({
		method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details',
		args: {
			"document": doc,
			"foreign_buyer": foreign_buyer,
			"final_destination": final_destination
		},
		async: false,
		callback: function(r) {
			if (r.message) {
				// console.log(r.message)
				cont_details = r.message
			}
		}
	})
	return cont_details
}

function check_for_existing(foreign_buyer, final_destination) {
  var print;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.container.container.validate_container_exist',
    args: {
      "foreign_buyer": foreign_buyer,
      "final_destination": final_destination
    },
    async: false,
    callback: function(r) {
      if(r.message){
        // console.log(r.message[0]["name"])
        print = r.message
      }
    }
  })
  return print
}

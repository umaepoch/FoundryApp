// Copyright (c) 2016, yashwanth and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.query_reports["Sales Order"] = {
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
			"options": "Port Of Dispatch"
		}
	],
	onload: function(report) {
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
						"options": "Port Of Dispatch",
        				"reqd": 1,
					},
				],
				primary_action: function(){
					d.hide()
					// console.log(d.get_value("foreign_buyer"))
					var foreign_buyer = frappe.query_report.get_filter_value("foreign_buyer")
					var final_destination = frappe.query_report.get_filter_value("final_destination")
					console.log(foreign_buyer)
					console.log(final_destination)
					var msg = validate(foreign_buyer, final_destination)
					console.log(msg)
					if (msg.length > 0) {
						var existing = ""
	          msg.forEach((cont)=> {
	            existing += cont["name"]+" "
	          })
						frappe.confirm(`The Following Container Plans ${existing} exist for this combination that has not been Finalized yet. Do you want to work with that Document?`,
	            () => {
	              // action to perform if Yes is selected
	            }, () => {
	              // action to perform if No is selected
								frappe.set_route("Form/Container/New Container",{"foreign_buyer": foreign_buyer, "final_destination": final_destination})
	            })
	        }
					if (msg.length == 0) {
						frappe.set_route("Form/Container/New Container",{"foreign_buyer": foreign_buyer, "final_destination": final_destination})
					}
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

// function fetch_so_details(foreign_buyer,final_destination)
// {
//
//     console.log("entered into function");
//     var selected_so= "";
//     frappe.call({
//         method: 'foundryapp.foundryapp.doctype.container.container.fetch_so_details',
//         args: {
//            "foreign_buyer":foreign_buyer,
//             "final_destination":final_destination
//         },
//         async: false,
//         callback: function(r) {
//             if (r.message) {
//                 // console.log(r.qty);
//                 selected_so = r.message;
//
//                 console.log(selected_so);
//                 console.log("readings-----------" + JSON.stringify(r.message));
//
//             }
//         }
//     });
//     return selected_so;
// }

function validate(foreign_buyer, final_destination) {
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

// Copyright (c) 2021, yashwanth and contributors
// For license information, please see license.txt



// Dynamic date chnage for week start date
frappe.ui.form.on('Committed Production Plan','week_start_date', function(frm, cdt, cdn){
	var cmp = locals[cdt][cdn]
	var week_start_date = cmp.week_start_date

	if (week_start_date) {
		check_foundry_settings('week_start_date', week_start_date)
		var end_date = ""
		var date = new Date(week_start_date)
		var new_date = new Date(date.getTime() + (6 * 24 * 60 * 60 * 1000))

		if (new_date) {
			end_date += new_date.getFullYear()

			if (new_date.getMonth() < '9') {
				let month = new_date.getMonth()+1
				end_date += "-"
				end_date +="0"+month
				end_date += "-"
			} else {
				let month = new_date.getMonth()+1
				end_date += "-"
				end_date += month
				end_date += "-"
			}

			if (new_date.getDate() <= '9') {
				let date = new_date.getDate()
				end_date += "0"+date
			} else {
				end_date += new_date.getDate()
			}

		}
		// console.log(doc)
		cur_frm.set_value('week_end_date', end_date)
		refresh_field('week_end_date')
	}
});

// Dynamic date change for week end date.
frappe.ui.form.on('Committed Production Plan','week_end_date', function(frm, cdt, cdn){
	var cmp = locals[cdt][cdn]
	var week_end_date = cmp.week_end_date

	if (week_end_date) {
		check_foundry_settings('week_end_date', week_end_date)
		var start_date = ""
		var date = new Date(week_end_date)
		var new_date = new Date(date.getTime() - (6 * 24 * 60 * 60 * 1000))

		if (new_date) {
			start_date += new_date.getFullYear()

			if (new_date.getMonth() < '9') {
				let month = new_date.getMonth()+1
				start_date += "-"
				start_date +="0"+month
				start_date += "-"
			} else {
				let month = new_date.getMonth()+1
				start_date += "-"
				start_date += month
				start_date += "-"
			}

			if (new_date.getDate() <= '9') {
				let date = new_date.getDate()
				start_date += "0"+date
			} else {
				start_date += new_date.getDate()
			}

		}
		cur_frm.set_value('week_start_date', start_date)
		refresh_field('week_start_date')
	}
});

// API call to frappe client to check for weekly start and end days.
// @parameter <planning cycle>, <date>
function check_foundry_settings(day_of_week, date) {
	var week_day = {
						'Sunday': 0, 'Monday': 1, 'Tuesday': 2,
		 				'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6
					}

	frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "FoundryApp Settings",
        },
        callback: function(r) {
            if(r.message) {
							if (day_of_week === 'week_start_date') {
								let day = new Date(date).getDay()

								if (day !== week_day[r.message.weekly_planning_cycle_begins_on]) {
									frappe.throw(__(`Please set date according to the FoundryApp Settings
																	<br>week_start_day: ${r.message.weekly_planning_cycle_begins_on}
																	, week_end_day: ${r.message.weekly_planning_cycle_ends_on}`))
								}
							}
							if (day_of_week === 'week_end_date') {
								let day = new Date(date).getDay()

								if (day !== week_day[r.message.weekly_planning_cycle_ends_on]) {
									frappe.throw(__(`Please set date according to the FoundryApp Settings
																	<br>week_start_day: ${r.message.weekly_planning_cycle_begins_on}
																	, week_end_day: ${r.message.weekly_planning_cycle_ends_on}`))
								}
							}
            }
        }
    });
}


// Dynamic table for child with start and end date, dispatch items.
frappe.ui.form.on('Committed Production Plan','get_items', function(frm, cdt, cdn) {
	 var cmp = locals[cdt][cdn]
   var week_start_date = cmp.week_start_date
   var week_end_date = cmp.week_end_date

   if (week_start_date && week_end_date) {
     var cmp_items = fetch_cmp_dispatch_items(week_end_date)
		 if (cmp_items) {
			 cmp_items.forEach((item) => {
				 var child = cur_frm.add_child('items');
				 console.log(item)
				 frappe.model.set_value(child.doctype, child.name, "start_date", week_start_date);
				 frappe.model.set_value(child.doctype, child.name, "week_ending", week_end_date);
				 frappe.model.set_value(child.doctype, child.name, "dispatch_item", item['item_code']);
				 frappe.model.set_value(child.doctype, child.name, "dispatch_item_name", item['item_name'])

				 if (item['so_requirement'] && item['avg_prod_req_per_day']) {
					 frappe.model.set_value(child.doctype, child.name, "so_requirement", item['so_requirement'])
					 frappe.model.set_value(child.doctype, child.name, "average_production_required_per_day", item['avg_prod_req_per_day'])
				 }

				 if (item['cont_requirement'] && item['avg_prod_req_per_day_cont']) {
					 frappe.model.set_value(child.doctype, child.name, "container_plan_requirement", item['cont_requirement'])
					 frappe.model.set_value(child.doctype, child.name, "average_production_required_per_day_container", item['avg_prod_req_per_day_cont'])
				 }

				 cur_frm.refresh_field("items");
			 });
		 }
   } else {
     frappe.throw(__("Please select both week start and end date"))
   }
});

// API call to python for fetching the dispatch cmp_items.
//@parameter	NONE.
//@return		dispatch items <ArrayJSON>.
function fetch_cmp_dispatch_items(week_end_date) {
  var items;
  frappe.call({
    method: 'foundryapp.foundryapp.doctype.committed_production_plan.committed_production_plan.fetch_cmp_items',
		args: {
			"week_end_date": week_end_date
		},
    async: false,
    callback: function(r) {
      if (r.message) {
				if (r.message.Exception) {
					frappe.throw(__(r.message.Exception))
				} else {
					console.log(r)
					items = r.message
				}
      }
    }
  });
  return items
}



// validation of committed production plan
frappe.ui.form.on('Committed Production Plan','validate', function(frm, cdt, cdn) {
	var cmp = locals[cdt][cdn]
	var week_start_date = cmp.week_start_date
	var week_end_date = cmp.week_end_date

	console.log(cmp)
	if (cmp.__unsaved === 1 && cmp.name.substring(0,4) === 'CMP-') {
		if (week_start_date && week_end_date) {
			var cur_doc_name = cmp.name
			var active_doc = check_for_active_cmp(week_start_date, week_end_date)
			if (active_doc.name && active_doc.is_active === 1 && active_doc.name !== cur_doc_name) {
				frappe.throw(__(`An Active Duplicate Document(${active_doc.name}) Already exists for the week ${active_doc.week_start_date} to ${active_doc.week_end_date}.`))
			}
		}
	}

	if (cmp.__unsaved === 1 && cmp.name.substring(0,4) !== 'CMP-') {

		if (cmp.is_active === 1 || cmp.is_active === 0) {

			if (week_start_date && week_end_date) {
				var active_doc = check_for_active_cmp(week_start_date, week_end_date)

				if (active_doc) {

						if (active_doc.is_active === 1) {
							var action = 0
							let d = new frappe.ui.Dialog({
									title: `A Active Document already esists for the Week<br>${active_doc.week_start_date} to ${active_doc.week_end_date}.<br>Do you want to:`,
									'fields': [
										{
											"fieldname": "Edit",
											"label": __("edit_html"),
											"fieldtype": "HTML",
											"options": "Edit the Active Document?"
										},
										{
											"fieldname": "Or",
											"label": __("or_html"),
											"fieldtype": "HTML",
											"options": "Or",
										},
										{
											"fieldname": "Duplicate",
											"label": __("duplicate_html"),
											"fieldtype": "HTML",
											"options": "Duplicate the Active Document into another Committed Production Plan Document and make the New Document Active?",
										},
									],
									primary_action_label: 'Edit',
									secondary_action_label: 'Duplicate',
									primary_action: function(values) {
											action += 1

											if (action === 1) {
												// console.log("primary");
												if (active_doc.name) {
													frappe.set_route('Form/Committed Production Plan/'+active_doc.name)
													d.hide()
												}
											}
									},
									secondary_action: function(values) {
											action += 2

											if (action === 2) {
												// console.log("Secondary");
												var duplicate_doc = duplicate_active_document(active_doc.name)
												// console.log(duplicate_doc)
												if (duplicate_doc.name) {
													frappe.set_route('Form/Committed Production Plan/'+duplicate_doc.name)
													d.hide()
												}
											}
									}
									});
									d.show();
									frappe.validated = false;
							}
					}
				}
			}
	}

});

// API call to python for validating existing doc for a week.
//@parameter <week start date>, <week end date>
//@return <document name>, <week start date>, <week end date>
function check_for_active_cmp(start_date, end_date) {
	let is_active;
	frappe.call({
		method: 'foundryapp.foundryapp.doctype.committed_production_plan.committed_production_plan.check_for_active_cmp',
		args: {
			'week_start_date': start_date,
			'week_end_date': end_date
		},
		async: false,
		callback: function(r) {
			if (r.message) {
				if (r.message.Exception) {
					frappe.throw(__(r.message.Exception))
				} else {
					is_active = r.message
					// console.log(r.message)
				}
			}
		}
	});
	return is_active
}

// API call to python for validating existing doc for a week.
//@parameter <document>
//@return <duplicate new document>
function duplicate_active_document(doc_name) {
	let dup_doc;
	frappe.call({
		method:'foundryapp.foundryapp.doctype.committed_production_plan.committed_production_plan.duplicate_active_doc',
		args: {
			'cur_doc': doc_name
		},
		async: false,
		callback: function(r) {
			if (r.message) {
				if (r.message.Exception) {
					frappe.throw(_(r.message.Exception))
				} else {
					dup_doc = r.message
				}
			}
		}
	})
	return dup_doc
}



// calculate quantity_in_tonnes, average_production_per_day_units, average_production_per_day_tonnes based on production_quantity_committed.
frappe.ui.form.on('Committed Production Plan Items','production_quantity_committed', function(frm, cdt, cdn) {
	var items = locals[cdt][cdn]
	// console.log(items)
	get_quantity_tons(items)
	items.average_production_per_day_units = items.production_quantity_committed/6
})

// API call to client for fetching the weight per unti from Item Master.
// @parameter <Object>
function get_quantity_tons(items) {
	frappe.call({
    method:"frappe.client.get_value",
    args: {
        doctype:"Item",
        filters: {
            item_code: items.dispatch_item
        },
        fieldname:["weight_per_unit"]
    },
    callback: function(r) {
			if (r.message) {
				var qty_tons = items.production_quantity_committed * r.message.weight_per_unit / 1000
				// console.log(qty_tons)
				items.quantity_in_tonnes = qty_tons
				items.average_production_per_day_tonnes = qty_tons/6
			}
    }
	})
}

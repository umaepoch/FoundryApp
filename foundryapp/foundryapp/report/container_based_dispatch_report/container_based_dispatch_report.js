// Copyright (c) 2016, yashwanth and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Container Based Dispatch Report"] = {
	"filters": [
		{
			"fieldname": "container",
			"label": __("Container"),
			"fieldtype": "Link",
			"options": "Container"
		}
	]
};

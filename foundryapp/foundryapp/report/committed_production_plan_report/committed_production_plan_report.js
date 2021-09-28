// Copyright (c) 2016, yashwanth and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Committed Production Plan Report"] = {
	"filters": [
		{
			'fieldname': 'committed_production_plan',
			'label': __('Committed Production Plan'),
			'fieldtype': 'Link',
			'options': 'Committed Production Plan'
		}
	]
};
